#! /usr/bin/python3

import sys
import threading

from socket import *

PORT = sys.argv[1]

server_sock = socket()

server_addr = ("0.0.0.0", int(PORT))
server_sock.bind(server_addr)

server_sock.listen(5)

def worker(sock):

	print("Building new thread")

	data = conn_sock.recv(1024)
	if data:
		print("Data received!")
		print(data.decode())

		sock.sendall(data)

	message = input()
	if message == "exit":
		return

	sock.close()

while True:
	(conn_sock, conn_addr) = server_sock.accept()
	threading.Thread(target = worker, args = (conn_sock,)).start()
