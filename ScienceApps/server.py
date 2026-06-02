import http.server
import os

APPS = {
    '/':          '/Users/f.cinar/Desktop/ScienceApps',
    '/biolab':    '/Users/f.cinar/Desktop/BioLab',
    '/chembase':  '/Users/f.cinar/Desktop/ChemBase',
    '/physdata':  '/Users/f.cinar/Desktop/PhysData',
    '/medcalc':   '/Users/f.cinar/Desktop/MedCalc',
    '/mathtool':  '/Users/f.cinar/Desktop/MathTool',
    '/weaponevo': '/Users/f.cinar/Desktop/WeaponEvo',
}

class MultiAppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.rstrip('/')
        for prefix, app_dir in APPS.items():
            if prefix == '/':
                if path == '' or path == '/':
                    os.chdir(app_dir)
                    self.path = '/index.html'
                    return http.server.SimpleHTTPRequestHandler.do_GET(self)
            elif path == prefix or path.startswith(prefix + '/'):
                os.chdir(app_dir)
                self.path = path[len(prefix):] or '/'
                if self.path == '/':
                    self.path = '/index.html'
                full_path = app_dir + self.path
                if not os.path.isfile(full_path):
                    self.path = '/index.html'
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
        self.send_error(404)

    def log_message(self, format, *args):
        pass

port = 3457
os.chdir(APPS['/'])
httpd = http.server.HTTPServer(('', port), MultiAppHandler)
print(f"Science Apps Server auf Port {port}")
httpd.serve_forever()
