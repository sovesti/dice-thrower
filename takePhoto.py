#! /usr/bin/env python

import os, re, sys, time, socket
camaddr = "192.168.42.1"
camport = 7878


def auth():
	data = srv.recv(512)
	# print('REQUEST_1: {"msg_id":257,"token":0}\n')
	# print("RESULT_1: " + data + " \n")
	if b"rval" in data:
		token = re.findall(b'"param": (.+) }',data)[0]	
	else:
		data = srv.recv(512)
		# print("RESULT_2: " + data)
		if b"rval" in data:
			token = re.findall(b'"param": (.+) }',data)[0]
	return token

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.connect((camaddr, camport))

srv.send(b'{"msg_id":257,"token":0}')
token = auth()

tosend = b'{"msg_id":769,"token":%s}' %token
srv.send(tosend)
# res = srv.recv(512)
# print('REQUEST_3: '+tosend+'\n')
# print("RESULT_3: " + res + " \n")