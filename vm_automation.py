from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import subprocess
import shutil

hostName = "localhost"
hostPort = 9001


pathFormat = "-nogui=/home/user/Desktop/simulation_topology/{number}/SDN-WISE-{number}-T{id}.csc"
RunPathFormat = "-nogui=/home/user/Desktop/simulation_topology/{number}/tmp/SDN-WISE-{number}-T{id}.csc"

class MyServer(BaseHTTPRequestHandler):
    procCtrl = None

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if MyServer.procCtrl != None:
            MyServer.procCtrl.kill()
        if self.headers.get('applypath') != None:
            ids = self.headers.get('applypath').split(':')
            self.move_tmp_file(ids=ids)
            self.run_cooja(ids=ids)
    def move_tmp_file(self, ids):
        shutil.copy(pathFormat.format(number=ids[0], id=ids[1]), RunPathFormat.format(number=ids[0], id=ids[1]))

    def run_cooja(self, ids):
        MyServer.procCtrl = subprocess.Popen(
            ['java', '-jar', '/home/user/contiki/tools/cooja/dist/coojar.jar',
             RunPathFormat.format(number=ids[0], id=ids[1])])
        print("PID fore ctrl:", MyServer.procCtrl.pid)


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))