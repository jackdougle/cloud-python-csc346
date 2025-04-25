#! /usr/bin/python3

import cgi
import os

form = cgi.FieldStorage()

if "text" in form:
	text = form["text"].value
else:
	text = None

try:
	s = form["size"].value
	size = int(s)
except:
	size = None

request_type = os.environ.get("REQUEST_METHOD")

if text is None or size is None or size < 0:
	print("Status: 400 Bad Request")
	print("Content-Type: text/html")
	print()

	print("<html>")
	print("<head><title>request_method_post.py</title></head>")
	print("<body>")
	print("<p>400 Bad Request<p>")
	print("<p>Input variables 'text' and 'size'</p>")
	print("</body>")
	print("</html>")

elif request_type != "POST":
	print("Status: 405 Method Not Allowed")
	print("Allow: POST")
	print()

	print("<html>")
	print("<head><title>request_method_post.py</title></head>")
	print("<body>")
	print("<p>405 Method Not Allowed</p>")
	print("<p>Use POST method</p>")
	print("</body>")
	print("</html>")

else:
	print("Status: 200 OK")
	print("Content-Type: text/html")
	print()

	print("<html>")
	print("<head><title>request_method_post.py</title></head>")

	print("<body>")
	print("<table>")

	for i in range(size):
		print("<tr>")
		for j in range(size):
			if ((i % 2) + j) % 2 == 0:
				print(f"<td>{text}</td>")
			else:
				print("<td>   </td>")
		print("</tr>")

	print("</table>")

	print("</body>")
	print("</html>")