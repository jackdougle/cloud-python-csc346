#! /usr/bin/python3

import cgi

form = cgi.FieldStorage()
if "number" in form:
	number = form["number"].value
else:
	number = None

print("Status: 200 OK")
print("Content-Type: text/html")
print("")

print("<html>")
print("<head><title>calculations</title></head>")
print("<body>")

if number == None:
	print("<p>The variable 'number' was not sent as a parameter</p>")
else:
	try:
		num = int(number)
	except:
		print(f"<p>The variable 'number', which was set to '{number}', cannot be converted to an integer</p>")
	else:
		num2 = num * num
		print(f"<p>The number is {num} <br> Its square is {num2}</p>")

print("</body>")
print("</html>")