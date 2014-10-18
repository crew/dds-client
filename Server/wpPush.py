from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import json

ADDR = "0.0.0.0"
PORT = 12345

class RequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    
    if 'content-length' not in self.headers:
      print 'ERROR:No content len in post request, exiting'
      return
    
    #get the data
    data = self.rfile.read(int(self.headers.getheader('content-length')))
    
    #print the data
    print json.loads(data)

    

httpd = HTTPServer((ADDR, PORT), RequestHandler)
httpd.serve_forever()