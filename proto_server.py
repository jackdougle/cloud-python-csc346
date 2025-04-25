#! /usr/bin/python3

import sys

from socket import *

HOST = sys.argv[1]
PORT = sys.argv[2]

sock = socket()

addr = (HOST, int(PORT))
sock.connect(addr)

def do_client(sock):
	message = "Hi from the client side!"
	sock.sendall(message.encode())

	data = sock.recv(64)
	if data:
		has_data = True
	else:
		has_data = False

	while has_data:
		print("Data received!")
		print(data.decode())
		print("\n")
		data = sock.recv(64)
		if data:
			has_data = True
		else:
			has_data = False

	sock.close()

do_client(sock)