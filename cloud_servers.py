#! /usr/bin/python3

import boto3
import cgi
import cgitb
import json
import MySQLdb
import os
from info import *
from access import *

cgitb.enable()

request = os.environ.get("REQUEST_METHOD")
path = os.environ.get("PATH_INFO")
dest = path[1:].split("/") if path else None

def status200(content):
	print("Status: 200 OK")
	if content == "json": print("Content-Type: application/json")
	elif content == "html": print("Content-Type: text/html")
	print()

def status400(msg):
	print("Status: 400 Bad Request")
	print("Content-Type: text/plain")
	print()

	print(msg)

conn = MySQLdb.connect(
	host=HOST,
	user=USER,
	port=PORT,
	passwd=PASS,
	db=NAME
)

form = cgi.FieldStorage()

if "remove" in form:
	remove = form["remove"].value

	cursor.execute("SELECT instanceID FROM servers WHERE id=%s", (remove))
	instance_to_rm = cursor.fetchone()
	cursor.execute("DELETE FROM servers WHERE id=%s", (remove))
	ec2 = boto3.client('ec2',
		region_name='us-east-1',
		aws_access_key_id=AWS_PUBLIC_KEY,
		aws_secret_access_key=AWS_SECRET_KEY)

	ec2.terminate_instances(InstanceIds=[instance_to_rm])
else:
	remove = None

cursor = conn.cursor()

def main():
	cursor.execute("SELECT * FROM servers")
	rows = cursor.fetchall()

	servers = []
	for row in rows:
		server = {}
		server["id"] = row[0]
		server["owner"] = row[1]
		server["description"] = row[2]
		server["instance"] = row[3]
		server["status"] = "live"
		if int(row[5]) == 1:
			server["ip"] = row[4]
		servers.append(server)

	if path is None:
		status200("html")
		print("<html><head><title>CloudServersMain</title></head>")
		print("<body>")
		print("<h1>Welcome to cloud_servers.py!</h1>")
		print("<p>Here you can launch an AWS EC2 Virtual Machine, monitor its state, and terminate it</p>")
		print("<h1>Create a VM!</h1>")
		print("<form action='create_server.py' method='get'>")
		print("Add a description for your server: <input type='text' name='desc' size=10>")
		print("<input type='submit' value='Create New VM'>")
		print("<h1>Terminate a VM!</h1>")
		print("<form action='cloud_servers.py' method='get'>")
		print("ID of VM being terminated: <input type='text' name='remove' size=10>")
		print("<input type='submit' value='Terminate VM'>")
		print("</form>")
		print("</body></html>")

	elif path == "/api":
		status400("Please specify API database")

	elif path == "/api/servers":
		status200("json")
		print(json.dumps(servers, indent=2))

	elif len(dest) == 3 and dest[0] == "api" and dest[1] == "servers":
		id = int(dest[2])
		cursor.execute("SELECT * FROM servers WHERE id=%s", (id,))
		result = cursor.fetchone()

		if result is None:
			status400(f"Please input a valid server ID instead of '{id}'")
			return

		else:
			server = {}
			server["id"] = result[0]
			server["owner"] = result[1]
			server["description"] = result[2]
			server["instance"] = result[3]
			server["status"] = "live"
			if int(row[5]) == 1: server["ip"] = result[4]

			status200("json")
			print(json.dumps(server, indent=2))

	else:
		status400("Please input a valid web request")

main()
conn.commit()
cursor.close()
conn.close()
