from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import thread

from Classes.message import Message


# Defaults
ADDR = "0.0.0.0"
PORT = 12345
writeOut = None


#Expecting to receive something of the form
#{
#    "datetime" : "2014-11-30T22:04:15+00:00", # ISO 8601, Timestamp of this push
#    "action" : "add-slide",
#    "pies" : [
#        { "name" : "shepard" },
#        { "name" : "blueberry" }, # allows adding of new fields later on down the road
#    ],
#    "content"  : { # should definitely be an object for flex and forward compatibility
#        "ID" : 14, # WordPress Post ID
#        "Permalink" : "http://dds-wp..." # The URL to the Post; does not append
#                                         # ?pie=name or anything fancy, just the permalink
#        # ... All other WordPress Post Fields... basically json_encode( get_post( $post_id ) )
#
#        # ... and then the post meta for plugins and other cool add-ons
#        "meta" : {
#            "key1" : [ "value" ],
#            "key2" : [
#                "value1",
#                "value2",
#                3,
#                {
#                    "meta can be weird" : "remember that"
#                }
#            ]
#        }
#    }
#}



class RequestHandler(BaseHTTPRequestHandler):
    """
    Handler Class for any requests received from WordPress
    @copyright: Northeastern University Crew 2014
    """

    def do_POST(self):
        """
        Handles received POST requests
        @return: None
        @rtype: NoneType
        """
        # writeOut is set externally to be the
        # socketServer Message Queue
        global writeOut
        if writeOut == None:
            # Receiving Queue has not been set
            print "(RequestHandler): writeOut is none. Returning."
            return
        if 'content-length' not in self.headers:
            # Malformed Header; content-length needed to know how many bytes to read
            print 'ERROR(RequestHandler): No content-length in post request, exiting'
            return

        # Read in the request
        data = self.rfile.read(int(self.headers.getheader('content-length')))

        # Log the request
        print "Http received POST: " + str(data)

        # Parse the request into JSON
        info = json.loads(data)

        for pie in info["pies"]:
            writeOut.put(
                Message("wpPush", pie["name"], "slideShow", info["action"], json.dumps(info["content"]),
                        info["datetime"]))

# Start the HTTP Server to receive any POST requests
# (Note: Python Server's Address set within WordPress Configuration)
httpd = HTTPServer((ADDR, PORT), RequestHandler)
thread.start_new_thread(httpd.serve_forever, ())

