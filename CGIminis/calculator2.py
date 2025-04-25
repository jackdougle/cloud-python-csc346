
#! /usr/bin/python3

import cgi

form = cgi.FieldStorage()
has_vars = True
bad_var = False

if "sum" in form:
	s = form["sum"].value
	try:
		sum = int(s)
	except:
		bad_var = True
else:
	sum = 0
	has_vars = False

if "count" in form:
	c = form["count"].value
	try:
		count = int(c)
	except:
		bad_var = True
else:
	count = -1  # set count to -1 so count is 0 after incremented for the first time
	has_vars = False

if "add" in form:
	a = form["add"].value
	try:
		add = int(a)
	except:
		bad_var = True
else:
	add = 0
	has_vars = False

if has_vars and bad_var:
	print("Status: 400 Bad Request")
	print("Content-Type: text/html")
	print()
	print("All inputs must be numbers")
else:
	print("Status: 200 OK")
	print("Content-Type: text/html")
	print()

	print("<html>")
	print("<head><title>averager</title></head>")
	print("<body>")

	sum += add
	count += 1

	print(f"<p>Sum = {sum}</p>")
	print(f"<p>Count = {count}</p>")
	print(f"<p>Added {add}</p>")
	avg = sum/count if (count > 0) else 0
	print(f"<p>The average is {avg}</p>")

	print("<form action='averager' method='post'>")
	print(f"<input type='hidden' name='sum' value={sum}>")
	print(f"<input type='hidden' name='count' value={count}>")
	print("New Number: <input type='text' name='add' size='10'>")
	print("<input type='submit' value='Add Number'>")
	print("</form>")

	print("</body>")
	print("</html>")