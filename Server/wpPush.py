from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import json

ADDR = "0.0.0.0"
PORT = 12345

class RequestHandler(BaseHTTPRequestHandler):
  def __init__(self, outboundMsgQueue):
	self.writeOut = outboundMsgQueue
	httpd = HTTPServer((ADDR, PORT), RequestHandler)
	httpd.serve_forever()

  def do_POST(self):
    
    if 'content-length' not in self.headers:
      print 'ERROR:No content len in post request, exiting'
      return
    
    #get the data
    data = self.rfile.read(int(self.headers.getheader('content-length')))
    
    #print the data
	print "Http recieved POST: "+str(data)
	
    info = json.loads(data)
	'''
	We must have recieved an input of JSON object with fields, pies, action, and content
	pies = a list of all the pies that have had a change
	action = add-slide || delete-slide || edit-slide (self explanatory)
	content = whatever is needed for the pies to process this request
	if action is add-slide => content = new slide
	if action is delete-slide => content = slide to delete
	if action is edit-slide => content = {"old" : [old slide], "new" : [new slide]}
	'''
	for pie in info["pies"]:
		self.writeOut.put(Message("wpPush", pie, "slideShow" , info["action"], info["content"]))
	
	#Could do some safety checks but I see them ass unnecessary
	# if info["action"] == "add-slide":
		# action = "loadSlides"
		# self.writeOut.put( 
	# elif info["action"] == "edit-slide":
		# action = "edit-slide"
		#refresh a slide
	# elif info["action"] == "-slide":
		# action = "delete-slide"
		#delete slide
	# else:
		# raise Exception("Recieved unknown action")

    

