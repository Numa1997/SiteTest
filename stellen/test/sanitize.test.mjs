// The mail cleaner (src/sanitize.js) against the attacks found in review and the classic ones.
import test from 'node:test';
import assert from 'node:assert/strict';
import { sanitizeMail, decodeEntities } from '../src/sanitize.js';

// Is every tag closed in order, and does nothing close what is outside the mail?
function balanced(html) {
  const stack = [];
  for (const m of html.matchAll(/<(\/?)([a-z0-9]+)[^>]*>/g)) {
    if (['br', 'col', 'hr', 'img', 'wbr'].includes(m[2])) continue;
    if (!m[1]) stack.push(m[2]);
    else if (stack.pop() !== m[2]) return false;
  }
  return stack.length === 0;
}

const cases = {
  'stray end tags try to leave the box': '</div></footer></article></main><div style="color:red">INJECTED</div>',
  'unfinished tag swallows what follows': "<p>ok</p><p title='",
  'unclosed link': '<a href="https://x.example/">click',
  'noembed hides the rest': '<p>sorry</p><noembed>',
  'xmp and plaintext': '<xmp><b>x</b></xmp><plaintext><div>rest',
  'script, also in odd spellings': '<script>alert(1)</script><SCRIPT SRC=//x.example/a.js></SCRIPT><scr<script>ipt>alert(1)</scr</script>ipt>',
  'event handlers': '<img src=x onerror=alert(1)><p onclick="alert(1)" ONMOUSEOVER=alert(1)>t</p><body onload=alert(1)>',
  'javascript links, encoded': '<a href="javascript:alert(1)">a</a><a href="&#106;avascript:alert(1)">b</a><a href="java&#x09;script:alert(1)">c</a><a href=" JaVaScRiPt:alert(1)">d</a><a href="data:text/html,x">e</a>',
  'style tricks': '<p style="position:fixed;top:0">a</p><p style="position:\\66ixed">b</p><p style="position/**/:fixed">c</p><p style="background:url(https://t.example/p.gif)">d</p><p style="width:expression(alert(1))">e</p><p style="color:red;transform:translate(-9999px)">f</p>',
  'forms, frames, objects, svg, math': '<form action=//x><input name=pw><button>go</button></form><iframe src=//x></iframe><object data=x></object><embed src=x><svg onload=alert(1)><a xlink:href=javascript:alert(1)>s</a></svg><math><mi>x</mi></math>',
  'comments, doctype, conditional comments': '<!DOCTYPE html><!--[if mso]><p>mso</p><![endif]--><!-- secret --><p>kept</p><?xml x?>',
  'remote and tracking images': '<img src="https://track.example/open.gif"><img src="http://x.example/a.png"><img srcset="https://x/a.png 1x">',
  'meta refresh, base, link': '<meta http-equiv="refresh" content="0;url=//x"><base href="//x/"><link rel=stylesheet href=//x/a.css>',
  'attribute quote break-out': '<p title="a&quot; onclick=&quot;alert(1)">t</p><p title=\'x" onclick="y\'>u</p>',
  'id and class clobbering': '<p id="m123" class="mail" name="x">t</p>',
};

test('every attack comes out inert and well-formed', () => {
  for (const [name, input] of Object.entries(cases)) {
    const out = sanitizeMail(input);
    assert.ok(balanced(out), name + ': not balanced: ' + out);
    for (const [what, bad] of [['script', /<script|<\/script/i], ['handler', /<[a-z0-9]+(?:\s+[a-z-]+="[^"]*")*\s+on[a-z]+=/i], ['javascript', /javascript:/i],
      ['frame', /<iframe|<frame|<object|<embed/i], ['form', /<form|<input|<button/i], ['svg', /<svg|<math/i], ['style block', /<style/i],
      ['meta/base/link', /<meta|<base|<link/i], ['remote src', /src="(?!data:|\/absagen\/img\/)/i], ['srcset', /srcset/i],
      ['url()', /url\(/i], ['fixed', /position\s*:/i], ['transform', /transform/i], ['comment', /<!--|secret|mso/],
      ['id/class/name', /<[a-z0-9]+(?:\s+[a-z-]+="[^"]*")*\s+(id|class|name)=/i], ['noembed/xmp', /<noembed|<xmp|<plaintext/i], ['data:text', /data:text/i]]) {
      assert.ok(!bad.test(out), `${name}: ${what} survived: ${out}`);
    }
  }
});

test('ordinary mail markup survives as it was written', () => {
  const png = 'data:image/png;base64,iVBORw0KGgo=';
  const input = '<html><head><title>t</title><style>p{color:red}</style></head><body><table width="600" cellpadding="0" style="border-collapse:collapse">' +
    '<tr><td align="center" style="padding:10px; font-family:Arial; color:#333">Sehr geehrter Herr Muster,<br>leider müssen wir Ihnen mitteilen &amp; bedauern &#8211; sehr.</td></tr>' +
    `</table><p><a href="https://firma.example/karriere?x=1&amp;y=2">Karriere</a> <img src="${png}" alt="Logo" width="120"> <img src="cid:logo@x"></p></body></html>`;
  const out = sanitizeMail(input, cid => (cid === 'logo@x' ? '/absagen/img/aaaa000000000001/0' : null));
  assert.ok(balanced(out));
  assert.match(out, /<table width="600" cellpadding="0" style="border-collapse:collapse">/);
  assert.match(out, /<td align="center" style="padding:10px;font-family:Arial;color:#333">/);
  assert.match(out, /leider müssen wir Ihnen mitteilen &amp; bedauern &#8211; sehr\./);
  assert.match(out, /<a href="https:\/\/firma\.example\/karriere\?x=1&amp;y=2" target="_blank" rel="noopener noreferrer nofollow">Karriere<\/a>/);
  assert.match(out, /<img src="data:image\/png;base64,iVBORw0KGgo=" alt="Logo" width="120">/);
  assert.match(out, /<img src="\/absagen\/img\/aaaa000000000001\/0">/);
  assert.ok(!/<title|<style|<html|<body|<head/.test(out));
});

test('entities are decoded before links are judged', () => {
  assert.equal(decodeEntities('&#106;ava&#x73;cript&colon;'), 'javascript:');
  assert.equal(decodeEntities('a &amp; b &unknown; c'), 'a & b &unknown; c');
});

test('linear time: hostile mails are cleaned quickly', () => {
  for (const [name, evil] of [['unfinished tags', '<a "'.repeat(20000) + '<p title="' + 'x'.repeat(100000)],
    ['deep stack, unmatched end tags (review round 2)', '<b>'.repeat(50000) + '</i>'.repeat(50000)],
    ['deep stack, matched end tags', '<b>'.repeat(30000) + '</b>'.repeat(30000)]]) {
    const t = performance.now();
    const out = sanitizeMail(evil);
    const ms = performance.now() - t;
    assert.ok(ms < 300, `${name}: took ${ms.toFixed(0)} ms`);
    assert.ok(balanced(out), name + ': not balanced');
  }
});
