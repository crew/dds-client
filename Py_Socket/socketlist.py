import socket

class socketList:
	def __init__(self, pieMap, sockList, serverSocket):
		self.pieMap = pieMap
		self.sockList = sockList
		self.serverSocket = serverSocket

	def addSocket(self, sock):
		self.sockList.append(sock)

	def mapPie(self, sock, pieName):
		self.pieMap[pieName] = sock

	def removeSocket(self, sock):
 		sock.close()
		self.sockList.remove(sock)
		del self.pieMap[self.getPie(sock)]

	def broadcast(self, sock, msg):
    #Do not send the message to master socket and the client who has send us the message
		for socket in self.sockList:
		    if socket != self.serverSocket and socket != sock :
		    	self.sendMessage(sock, msg)

	def sendMessage(self, sock, msg):
		try :
			sock.send(msg)
		except :
			self.removeSocket(sock)

	def getSock(self, pie):
		return self.pieMap[pie]

	def getPie(self, sock):
		for pie, socket in self.pieMap:
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
