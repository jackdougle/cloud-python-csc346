#! /usr/bin/python3

import sys

from socket import *

HOST = sys.argv[1]
PORT = sys.argv[2]
MODE = sys.argv[3]

s_sock = socket()
c_sock = socket()

def start_socket(mode):

	if mode == "server":
		print("Building server")

		s_addr = ("0.0.0.0", int(PORT))

		s_sock.bind(s_addr)
		s_sock.listen(5)

		(conn_sock, conn_addr) = s_sock.accept()

		while True:
			data = conn_sock.recv(1024)
			print("Data received by server!")
			print(data.decode())
			if data.decode() == "exit":
				break

			message = input("Send a message to the client: ")
			conn_sock.sendall(message.encode())
			if message == "exit":
				break

		print("Closing server")
		conn_sock.close()
		s_sock.close()

	elif mode == "client":
		print("Building client")

		c_addr = (HOST, int(PORT))

		c_sock.connect(c_addr)

		while True:
			message = input("Send a message to the server: ")
			c_sock.sendall(message.encode())
			if message == "exit":
				break

			data = c_sock.recv(1024)
			print("Data received by client!")
			print(data.decode())
			if data.decode() == "exit":
				break

		print("Closing client")
		c_sock.close()

	else:
		print("Invalid type")
		sys.exit(0)

start_socket(MODE)