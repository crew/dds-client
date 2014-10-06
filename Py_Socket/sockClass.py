import socket, time
from message import Message

class sockClass:
	def __init__(self, host, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.hostIP = host
		self.hostPort = port
		self.connect()

	def connect(self):
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
		identify = Message("blueberry", "Grandma", "connect",{})
		identify.add_content("name","blueberry")
		identify.add_content("item2","bob")
		self.sock.send(identify.toJSON())