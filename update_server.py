#! /usr/bin/python3

import boto3
import MySQLdb
import os
import time
from info import *
from access import *

import cgitb
cgitb.enable()

conn = MySQLdb.connect(
	host=HOST,
	port=PORT,
	user=USER,
	passwd=PASS,
	db=NAME
)

cursor = conn.cursor()

def monitor(server, ec2, instanceID):
	instance = ec2.Instance(instanceID)

	instance.wait_until_running()
	instance.reload()

	addressIP = instance.public_ip_address

	cursor.execute("UPDATE servers SET ready=%s WHERE instanceID=%s", (1, instanceID))
	cursor.execute("UPDATE servers SET addressIP=%s WHERE instanceID=%s", (addressIP, instanceID))

	# Download shit

conn.commit()
cursor.close()
conn.close()