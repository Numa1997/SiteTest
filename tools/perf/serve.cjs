// A local stand-in for how Cloudflare serves phyeinusul.com, for measuring before and after a change (docs/performance.md).
// node tools/perf/serve.cjs <folder> <port> [noredirect]       e.g. node tools/perf/serve.cjs dist 8080
// Like Cloudflare (measured 31 October 2026): Brotli for text files; the response headers of <folder>/_headers; a weak ETag and
// 304 answers for every file except HTML, which Cloudflare sends with no ETag; Cache-Control public, max-age=0, must-revalidate
// unless _headers says otherwise; a request for x.html answered 307 -> x (and x/index.html -> x/), x answered with x.html.
// It listens on 127.0.0.1 only and serves nothing outside <folder>.
// H2=1 serves HTTP/2 over TLS, as phones reach Cloudflare; it makes (with openssl) a throwaway self-signed certificate in the system's temporary
// folder (browsers keep no cache for a page with a certificate error, so time repeat visits over plain HTTP).
const http=require('http'),http2=require('http2'),fs=require('fs'),path=require('path'),zlib=require('zlib'),crypto=require('crypto');
const root=path.resolve(process.argv[2]||'dist'),port=+process.argv[3]||8080, redirectHtml=process.argv[4]!=='noredirect';
function rules(){const t=fs.existsSync(root+'/_headers')?fs.readFileSync(root+'/_headers','utf8'):'';const out=[];let cur=null;
 for(const l of t.split('\n')){if(/^\s*#/.test(l)||!l.trim())continue; if(!/^\s/.test(l)){cur={pat:l.trim(),h:[]};out.push(cur);} else {const i=l.indexOf(':');cur.h.push([l.slice(0,i).trim(),l.slice(i+1).trim()]);}}
 return out;}
function match(p,u){const re=new RegExp('^'+p.split('*').map(s=>s.replace(/[.+?^${}()|[\]\\]/g,'\\$&')).join('.*')+'$');return re.test(u);}
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.woff2':'font/woff2','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.json':'application/json','.txt':'text/plain','.jpg':'image/jpeg'};
const cache={};
const realRoot=fs.realpathSync(root), inRoot=q=>q===realRoot||q.startsWith(realRoot+path.sep);
const handler=(req,res)=>{try{serveOne(req,res);}catch(e){try{res.writeHead(500);res.end('error');}catch(e2){}}};   // one request never ends the server
const serveOne=(req,res)=>{let u; const qs=req.url.includes('?')?req.url.slice(req.url.indexOf('?')):''; try{u=decodeURIComponent(req.url.split('?')[0]);}catch(e){res.writeHead(400);return res.end('bad address');}
 if(u.includes('\0')){res.writeHead(400);return res.end('bad address');}
 u=path.posix.normalize('/'+u);   // from here on only the normalized path: no '..' can remain in it
 if(u==='/_headers'){res.writeHead(404);return res.end('nf');}   // Cloudflare reads _headers and never serves it
 if(redirectHtml&&u.endsWith('.html')){let t=u.slice(0,-5); if(t.endsWith('/index'))t=t.slice(0,-5); res.writeHead(307,{location:encodeURI(t)+qs});return res.end();}
 let f=path.join(root,u); if(u.endsWith('/'))f=path.join(f,'index.html'); else if(!fs.existsSync(f)||fs.statSync(f).isDirectory()){ if(fs.existsSync(f+'.html'))f+='.html'; else if(fs.existsSync(path.join(f,'index.html'))){res.writeHead(307,{location:encodeURI(u+'/')+qs});return res.end();} }
 if(!fs.existsSync(f)||fs.statSync(f).isDirectory()){res.writeHead(404);return res.end('nf');}
 if(!inRoot(fs.realpathSync(f))){res.writeHead(403);return res.end('outside');}   // nothing outside <folder>, links included
 const st=fs.statSync(f),key=f+st.mtimeMs; if(!cache[key]){const b=fs.readFileSync(f);const ext=path.extname(f);const comp=/\.(html|css|js|svg|json|txt)$/.test(f);cache[key]={b,br:comp?zlib.brotliCompressSync(b,{params:{[zlib.constants.BROTLI_PARAM_QUALITY]:5}}):null,etag:'W/"'+crypto.createHash('md5').update(b).digest('hex')+'"',type:types[ext]||'application/octet-stream'};}
 const c=cache[key]; const isHtml=f.endsWith('.html'); const h={'content-type':c.type,'cache-control':'public, max-age=0, must-revalidate'}; if(!isHtml)h.etag=c.etag;
 for(const r of rules()) if(match(r.pat,u)) for(const [k,v] of r.h) h[k.toLowerCase()]=v;
 if(!isHtml&&req.headers['if-none-match']===c.etag){res.writeHead(304,h);return res.end();}
 if(c.br&&/br/.test(req.headers['accept-encoding']||'')){h['content-encoding']='br';res.writeHead(200,h);return res.end(c.br);}
 res.writeHead(200,h);res.end(c.b);
};
if(process.env.H2){(()=>{const d=require('os').tmpdir(),k=d+'/perf-serve-key.pem',c=d+'/perf-serve-cert.pem'; if(!fs.existsSync(c)) require('child_process').execSync(`openssl req -x509 -newkey rsa:2048 -nodes -keyout ${k} -out ${c} -days 30 -subj /CN=localhost`,{stdio:'ignore'}); return http2.createSecureServer({key:fs.readFileSync(k),cert:fs.readFileSync(c),allowHTTP1:true},handler);})().listen(port,'127.0.0.1',()=>console.log('h2 serving',root,'on https://127.0.0.1:'+port));}
else http.createServer(handler).listen(port,'127.0.0.1',()=>console.log('serving',root,'on http://127.0.0.1:'+port));
