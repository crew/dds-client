import socket, time

class socketList:
	def __init__(self, pieMap, sockList, serverSocket):
		self.pieMap = pieMap
		self.sockList = sockList
		self.serverSocket = serverSocket

	def addSocket(self, sock):
		self.sockList.append(sock)

	def mapPie(self, sock, pieName):
		print "mapping" + pieName
		self.pieMap[pieName] = sock

	def removeSocket(self, sock):
		print "Good bye!"
 		sock.close()
		self.sockList.remove(sock)
		print(self.getPie(sock))
		self.pieMap.pop(self.getPie(sock))

	def broadcast(self, sock, msg):
    #Do not send the message to master socket and the client who has send us the message
		for socket in self.sockList:
			print(self.getPie(socket))
			if socket != self.serverSocket and socket != sock:
				self.sendMessage(socket, msg)

	def sendMessage(self, sock, msg):
		print "Sending"
		print str(sock) + " Peer name : "+str(sock.getpeername())
		print "Message "+str(msg)
		try :
			sock.sendall(msg)
			print "Message sent!"
			#stops here when slide doesn't make it?
		except Exception as e:
			print str(e)
			self.removeSocket(sock)

	def getSock(self, pie):
		return self.pieMap[pie]

	def getPie(self, sock):
		print(len(self.pieMap))
		for pie, socket in self.pieMap.iteritems():
			if sock == socket:
				return pie

	# def broadcastToAll(self, index, message):
	# 	for i in index:
	# 		self.broadcast(i, message);

	# # def readFromSocket(self, index):
	# # 	try:
	# # 		# sockets[index].read(message)
	# # 	except :
	# # 		self.removeSocket(pieName)
	# # 		#connection lost exception

	# # def connectionLost(self, index):
	# # 	self.sockets.remove(index)
