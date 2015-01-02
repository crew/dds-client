import socket, time
from message import Message

class sockClass:
	""" Client Socket class. Lets us split off socket functionality into 
	multiple threads such that we can send and recive sockets comunications
	without any troubles."""
	def __init__(self, runtimeVars):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.hostIP = runtimeVars["server"]
		self.hostPort = int(runtimeVars["port"])
		self.connect(runtimeVars)

	def send(self, msg):
		self.sock.send(msg)

	def connect(self, runtimeVars):
		print "Im conected: "+runtimeVars["name"]
		while True:
			# connect to remote host
			#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#s.settimeout(2)
			try :
				self.sock.connect((self.hostIP, self.hostPort))
				print "Connected"
				break
			except :
				print 'Unable to connect'
				time.sleep(2)

		# Passes along PIE name to Grandma
		# Needs to be abstracted to allow config setting of these parameters
		identify = Message(runtimeVars["name"], "Grandma","socketServer" , "connect",{})
		identify.add_content("name",runtimeVars["name"])
		identify.add_content("item2","bob")
		self.sock.send(identify.toJSON() + '\v')
