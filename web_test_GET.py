#! /usr/bin/python3

import cgi
import os
import sys

form = cgi.FieldStorage()

if "asdf" in form:
	asdf = form["asdf"].value
else:
	asdf = None

if "jkl" in form:
	jkl = form["jkl"].value
else:
	jkl = None

request_type = os.environ.get("REQUEST_METHOD")

if asdf is None or jkl is None:
	print("Status: 400 Bad Request")
	print("Content-Type: text/html")
	print()

	print("<html>")
	print("<head><title>request_method_get.py</title></head>")
	print("<body>")
	print("<p>400 Bad Request</p>")
	print("<p>Input variables 'asdf' and 'jkl'</p>")
	print("</body>")
	print("</html>")

elif request_type != "GET":
	print("Status: 405 Method Not Allowed")
	print("Allow: GET")
	print("Content-Type: text/html")
	print()

	print("<html>")
	print("<head><title>request_method_get.py</title></head>")
	print("<body>")
	print("<p>405 Method Not Allowed</p>")
	print("<p>Use GET method</p>")
	print("</body>")
	print("</html>")

else:
	print("Status: 200 OK")
	print("Content-Type: text/html")
	print()

	print("<html>")
	print("<head><title>request_method_get.py</title></head>")
	print("<body>")

	for i in range(20):
		print(f"<p>asdf = {asdf}</p>")
		print(f"<p>jkl = {jkl}</p>")

	print("</body>")
	print("</html>")