'''
Created on Sep 12, 2014

@author: David
'''

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
 
 
class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    
    #opens a loop that waits for raw_input and sends it
    def open(self):
        print 'new connection'
        self.write_message("Hello World")
        while True:
            self.loop()
        
    def on_message(self, message):
        print 'message received %s' % message
 
    def on_close(self):
        print 'connection closed'
        
    def loop(self):
        message = raw_input('Enter message: ')
        self.write_message(message)
 
#creates tornado server
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
#starts tornado server
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(8888)
tornado.ioloop.IOLoop.instance().start()
