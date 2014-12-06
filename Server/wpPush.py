from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import json
import thread
from Classes.message import Message

ADDR = "0.0.0.0"
PORT = 12345
writeOut = None

class RequestHandler(BaseHTTPRequestHandler):



  def do_POST(self):
    global writeOut
    if writeOut == None:
      print "writeOut is none. Returning."
      return
    if 'content-length' not in self.headers:
      print 'ERROR:No content len in post request, exiting'
      return
    
    #get the data
    data = self.rfile.read(int(self.headers.getheader('content-length')))
    
    #print the data
    print "Http recieved POST: "+str(data)
	
    info = json.loads(data)
    '''
	Expecting to receive something of the form
	{
		"datetime" : "2014-11-30T22:04:15+00:00", # ISO 8601, Timestamp of this push
		"action" : "add-slide",
		"pies" : [ 
			{ "name" : "shepard" }, 
			{ "name" : "blueberry" }, # allows adding of new fields later on down the road
		],
		"content"  : { # should definitely be an object for flex and forward compat
			"ID" : 14, # WordPress Post ID
			"Permalink" : "http://dds-wp..." #The URL to the Post... does not append ?pie=name or anything fancy... just the permalink
			# ... All other WordPress Post Fields... basically json_encode( get_post( $post_id ) )

			# ... and then the post meta for plugins and other cool add-ons
			"meta" : { 
				"key1" : [ "value" ],
				"key2" : [ 
					"value1", 
					"value2", 
					3, 
					{ 
						"meta can be weird" : "remember that" 
					} 
				]
			}
		} 
	}
	'''
    for pie in info["pies"]:
        writeOut.put(Message("wpPush", pie["name"], "slideShow" , info["action"], json.dumps(info["content"]), info["datetime"]))
	
	#Could do some safety checks but I see them as unnecessary
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

    
httpd = HTTPServer((ADDR, PORT), RequestHandler)
thread.start_new_thread(httpd.serve_forever,())

