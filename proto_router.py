#! /usr/bin/python3

import random
import sys
import threading
import time

from socket import *

server_temp = ["", None]
server_info = ""
dest_temp = ["", None]
dest_info = ""

if len(sys.argv) > 2:
	server_info = sys.argv[1].split(":")
	dest_info = sys.argv[2].split(":")

	if server_info[0]:
		server_temp[0] = server_info[0]
	if server_info[1]:
		server_temp[1] = int(server_info[1])

else:
	dest_info = sys.argv[1].split(":")

if server_temp[0] == "":
	server_temp[0] = "0.0.0.0"
if server_temp[1] == None:
	server_temp[1] = random.randint(1024, 65535)

server_addr = tuple(server_temp)

server_sock = socket()
server_sock.bind(server_addr)

server_sock.listen(5)

dest_temp[0] = dest_info[0]
dest_temp[1] = int(dest_info[1])

dest_addr = tuple(dest_temp)

print(f"FORWARDING: {server_addr} --> {dest_addr}")

def external_path(conn_sock, dest_sock):

	while True:
		try:
			data = conn_sock.recv(1024)
		except:
			dest_sock.shutdown(socket.SHUT_WR)
			break

		if not data or data.decode() == "" or data.decode() == "exit":
			break

		print("Data received from client")
		print(data.decode())

		try:
			dest_sock.sendall(data)
		except:
			conn_sock.shutdown(SHUT_WR)
			break

		print("Data sent to server")

	print("Closing C --> S line")
	try:
		conn_sock.close()
		dest_sock.close()
	except:
		return

def internal_path(conn_sock, dest_sock):

	while True:
		try:
			data = dest_sock.recv(1024)
		except:
			conn_sock.shutdown(socket.SHUT_WR)
			break

		if not data or data.decode() == "" or data.decode() == "exit":
			break

		print("Data received from server")
		print(data.decode())

		try:
			conn_sock.sendall(data)
		except:
			dest_sock.shutdown(socket.SHUT_WR)
			break

		print("Data sent to client")

	print("Closing C <-- S line")
	try:
		conn_sock.close()
		dest_sock.close()
	except:
		return

while True:
	try:
		(conn_sock, conn_addr) = server_sock.accept()
		dest_sock = socket()
		dest_sock.connect(dest_addr)
	except:
		conn_sock.close()
		dest_sock.close()
		break

	print(f"New connection from {conn_addr}")
	threading.Thread(target = external_path, args = (conn_sock, dest_sock)).start()
	threading.Thread(target = internal_path, args = (conn_sock, dest_sock)).start()