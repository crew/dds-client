import urllib2

from Classes.message import Message
import wpPush

#inputQueue is info for this plugin
#queues are queues for every plugin
#runtimeVars is a dictionary containing all important information for this program
def main_WPHandler_thread(inputQueue, queues, runtimeVars):
	while True:
		if not inputQueue.empty():
			print "WPListener recieved a message"
			message = inputQueue.get()
			handle(message,queues["socketServer"], runtimeVars)
#Action: querySlides -> queries for the slides of a given pie
#         content = the name of the pie requesting its slides 
def handle(message, outputQueue, runtime):
	if message["action"] == "querySlides":
		pieName = message["src"]
		jsonToSend = querySlidesFor(pieName, runtime["server"])
		#TODO setup DT
		message = Message("WPHandler", pieName, "slideShow", "load-slides", jsonToSend)
		print "Wp sending message"
		outputQueue.put(message)
	#TODO more to come...

def wpListenerStart(outboundMessageQueue):
	print "Starting http POST server for wp updates"
        wpPush.writeOut = outboundMessageQueue

def querySlidesFor(pieName, url):
	url = "http://"+url+"/wp-admin/admin-ajax.php?action=dds_api&pie_name="+pieName
	jsonString = str(urllib2.urlopen(url).read().decode("utf-8"))
	print "Slides for " + pieName + ": " + jsonString
	return jsonString


#queues[socket] is a socket handler, hand it a message and the socket thread will send it accordingly
#Action = Send2Pie(?)
#content = slides info
