import urllib2

from Classes.message import Message
import wpPush


def main_WPHandler_thread(inputQueue, queues, runtimeVars):
    """
    The main thread for the WordPress Handler Plugin
    @param inputQueue: The Queue Responsible for receiving WPHandler messages
    @type inputQueue: Queue.Queue
    @param queues: The Global Queue Dictionary
    @type queues: QueueDict
    @param runtimeVars: User-Specified Configuration
    @type runtimeVars: Dictionary
    @return: None
    @rtype: NoneType
    @copyright: Northeastern University Crew 2014
    """
    while True:
        if not inputQueue.empty():
            print "WPListener received a message"
            message = inputQueue.get()
            handle(message, queues["socketServer"], runtimeVars)


def handle(message, outputQueue, runtime):
    """
    WPHandler Thread Message Handler
    @param message: The received message
    @type message: Message
    @param outputQueue: The queue to output any response to
    @type outputQueue: Queue.Queue
    @param runtime: User-Specified Configuration
    @type runtime: Dictionary
    @return: None
    @rtype: NoneType
    """
    if message["action"] == "load-slides":
        pieName = message["src"]
        jsonToSend = querySlidesFor(pieName, runtime["server"])
        message = Message("WPHandler", pieName, "slideShow", "load-slides", jsonToSend)
        print "Wp sending message"
        outputQueue.put(message)


def wpListenerStart(outboundMessageQueue):
    """
    Sets the given queue as the receiver for any processed POST
    Requests sent out from the WordPress Server
    @param outboundMessageQueue: The queue to receive WordPress Messages
    @type outboundMessageQueue: Queue.Queue
    @return: None
    @rtype: NoneType
    """
    print "Starting http POST server for wp updates"
    wpPush.writeOut = outboundMessageQueue


def querySlidesFor(pieName, url):
    """
    Retrieves a JSON string containing the slides for the
    given Raspberry Pi
    @param pieName: The name of the Raspberry Pi whose slides to retrieve
    @type pieName: String
    @param url: The Base URL of the WordPress Site
    @type url: String
    @return: A JSON Representation of the given Raspberry Pi's slides
    @rtype: String
    """
    url = "http://" + url + "/wp-admin/admin-ajax.php?action=dds_api&pie_name=" + pieName
    #jsonString = str(urllib2.urlopen(url).read().decode("utf-8"))
    jsonString = '''
{
    "actions":[
{
             "type":"slide",
             "location":"http://elk.ccs.neu.edu/app/kibana#/dashboard/7e8374b0-04dc-11e7-a330-7fbd3eb62fc4?_g=(refreshInterval%3A(display%3A'5%20minutes'%2Cpause%3A!f%2Csection%3A2%2Cvalue%3A300000)%2Ctime%3A(from%3Anow-12h%2Cmode%3Aquick%2Cto%3Anow))&embed=true",
             "duration":600,
             "ID":1
        }]}'''
    print "Slides for " + pieName + ": " + jsonString
    return jsonString

