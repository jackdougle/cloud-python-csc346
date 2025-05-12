#! /usr/bin/python3

import boto3  # this is the AWS SDK
import cgi
import cgitb
import MySQLdb
import os
import update_server
from info import *
from access import *

cgitb.enable()

form = cgi.FieldStorage()

desc = form["desc"].value if "desc" in form else None

#url = os.environ.get("HTTP_HOST") + os.environ.get("SCRIPT_NAME")
url = "http://localhost:8080/cgi-bin/cloud_servers.py"

conn = MySQLdb.connect(
	host=HOST,
	port=PORT,
	user=USER,
	passwd=PASS,
	db=NAME
)

cursor = conn.cursor()

def main():
	cursor.execute("SELECT MAX(id) FROM sessions")
	userID = cursor.fetchone()
	cursor.execute("SELECT user FROM sessions WHERE id=%s", (userID,))
	user = cursor.fetchone()[0]

	ec2_resource = boto3.resource('ec2',
			'us-east-1',
			aws_access_key_id=AWS_PUBLIC_KEY,
			aws_secret_access_key=AWS_SECRET_KEY)

	ec2_client = boto3.client('ec2',
			'us-east-1',
			aws_access_key_id=AWS_PUBLIC_KEY,
			aws_secret_access_key=AWS_SECRET_KEY)

	server = ec2_client.run_instances(InstanceType='t2.micro',
			MaxCount=1,
			MinCount=1,
			ImageId="ami-0f88e80871fd81e91",
			KeyName=AWS_KEY_PAIR_NAME,
			SecurityGroupIds=[AWS_SECURITY_GROUP_IDS])

	instanceID = server['Instances'][0]['InstanceId']

	cursor.execute("INSERT INTO servers (owner, instanceID) VALUES (%s, %s)", (user, instanceID))
	if desc: cursor.execute("UPDATE servers SET description=%s WHERE instanceID=%s", (desc, instanceID))
	conn.commit()
	# by default, ready = 0 and addressIP = NULL

	cursor.execute("SELECT MAX(id) FROM servers")
	serverID = cursor.fetchone()[0]

	print("Status: 303 Redirect")
	serverURL = f"{url}/api/servers/{serverID}"
	print(f"Location: {serverURL}")
	print()

	instance = ec2_resource.Instance(instanceID)

	instance.wait_until_running()
	instance.reload()

	addressIP = instance.public_ip_address

	cursor.execute("UPDATE servers SET ready=%s WHERE instanceID=%s", (1, instanceID))
	cursor.execute("UPDATE servers SET addressIP=%s WHERE instanceID=%s", (addressIP, instanceID))

main()
conn.commit()
cursor.close()
conn.close()
