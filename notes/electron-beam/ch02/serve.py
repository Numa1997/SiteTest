"""Static server for the preview: public/ is the site root; /__preview/ is notes/electron-beam/ch02/preview/.   python3 serve.py [port]"""
import http.server, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split('?', 1)[0]
        if p.startswith('/__preview/'): return os.path.join(HERE, 'preview', p[len('/__preview/'):] or 'index.html')
        return os.path.join(ROOT, 'public', p.lstrip('/'))
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 8765), H).serve_forever()
