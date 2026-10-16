"""Build a main-website copy from a checked-out AppDeploy project.

Usage: python3 make_portfolio_copy.py SOURCE WORKDIR

SOURCE is the complete app source, with its existing node_modules available.
WORKDIR must not exist. The generated dist/ is the website copy. The standalone
app is never edited. Install no dependencies; use the source's existing Vite.
"""
from pathlib import Path
import re,shutil,subprocess,sys

source=Path(sys.argv[1]).resolve()
work=Path(sys.argv[2]).resolve()
assert not work.exists(),f'Working directory already exists: {work}'
assert (source/'src/App.tsx').is_file()
shutil.copytree(source,work,ignore=shutil.ignore_patterns('node_modules','dist','.git'))
(work/'node_modules').symlink_to((source/'node_modules').resolve(),target_is_directory=True)
app=work/'src/App.tsx'
t=app.read_text()
for old in ("import Runs from './pages/Runs';\n",
            '            <NavLink to="/runs">Saved runs</NavLink>\n',
            '          <Route path="/runs" element={<Runs />} />\n'):
    assert t.count(old)==1,old
    t=t.replace(old,'')
anchor='        <div className="site-bar-i">'
assert t.count(anchor)==1
t=t.replace(anchor,anchor+'\n          <a href="../../portfolios.html" className="back-site">← Numa Koudsie · Portfolios</a>')
app.write_text(t)
(work/'src/pages/Runs.tsx').unlink()
sim=work/'src/pages/Simulate.tsx'
t=sim.read_text()
for old in ("import { api } from '@appdeploy/client';\n",
            "  const [name, setName] = useState('');\n"):
    assert t.count(old)==1,old
    t=t.replace(old,'')
t,count=re.subn(r'  const save = async \(\) => \{.*?\n  \};\n\n','',t,flags=re.S)
assert count==1
pattern=r'            \{(?:result|res) && \(\n              <div className="sim-form" style=\{\{ paddingTop: 12, borderTop:.*?\n            \)\}'
t,count=re.subn(pattern,'            <p className="note">This website copy runs in your browser. Saving named runs is available in the standalone project.</p>',t,flags=re.S)
assert count==1
assert '@appdeploy' not in t and 'onClick={save}' not in t
sim.write_text(t)
css=work/'src/index.css'
css.write_text(css.read_text()+'\n/* Main website navigation, outside the standalone app. */\n.back-site { color: var(--muted); font: 11px var(--mono); text-decoration: none; padding: 6px 0; }\n.back-site:hover { color: var(--wine); }\n')
index=work/'index.html'
t=index.read_text();t,count=re.subn(r'<title>(.*?)</title>',r'<title>\1 · Numa Koudsie</title>',t)
assert count==1;index.write_text(t)
config=work/'vite.website.config.ts'
config.write_text("import { defineConfig } from 'vite';\nimport react from '@vitejs/plugin-react';\nexport default defineConfig({ plugins: [react()], base: './', build: { assetsDir: 'static' } });\n")
subprocess.run(['node','node_modules/vite/bin/vite.js','build','--config',config.name],cwd=work,check=True)
index=work/'dist/index.html'
t=index.read_text()
def loader(m):
    return "<script>(function(){var l=document.createElement('link');l.rel='stylesheet';l.href='"+m.group(1)+"';document.head.appendChild(l)})();</script>"
t,count=re.subn(r'<link rel="stylesheet" crossorigin href="([^"]+)">',loader,t)
assert count==1
index.write_text(t)
print('Website copy:',work/'dist')
