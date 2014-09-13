#!/usr/bin/python

import socket
import json
from time import sleep

#data = ('hellow world')

#data = {'message':'hello world!', 'test':123.4}

while True: 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 13373))
	#s.send(json.dumps(data))
	prompt = raw_input("Input Data ")	
	s.send(prompt)
	result = s.recv(1024) #json.loads(s.recv(1024))
	print result
	sleep(5)
	
#s.close()
