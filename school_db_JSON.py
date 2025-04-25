#! /usr/bin/python3

import cgitb
import os
import json
import sys

cgitb.enable()

file = open("school.json", "r")
data = json.load(file)
file.close()

request = os.environ.get("REQUEST_METHOD")

url = os.environ.get("HTTP_HOST") + os.environ.get("SCRIPT_NAME")
dir = os.environ.get("PATH_INFO")

if dir != None:
	url += dir
	dest = dir[1:].split("/")
else:
	dest = None

def status200():
	print("Status: 200 OK")
	print("Content-Type: application/json")
	print()

def status303():
	print("Status: 303 Redirect")
	print(f"Location: {url}")
	print()

def status400(para=None, type=None, message=None):
	print("Status: 400 Bad Request")
	print("Content-Type: text/html")
	print()

	print("<html><body>")
	print("<p>400 Bad Request</p>")

	if message and message == "Invalid format":
		print(f"<p>The method is {request}, but the request body is not in valid JSON format</p>")
	elif message:
		print(f"<p>{message}</p>")
	elif isinstance(para, int):
		print(f"<p>{request} to {dir} must have exactly {str(para)} field(s): {type}</p>")
	elif para and type:
		print(f"<p>The {para} parameter must be a(n) {type}</p>")

	print("</body></html>")

def status404():
	print("Status: 404 Not Found")
	print("Content-Type: text/html")
	print()

	print("<html><body>")
	print("<p>Page not found, check URL</p>")
	print(f"<p>PATH_INFO: {dir}</p>")
	print("</body></html>")

def status405(methods):
	print("Status: 405 Method Not Allowed")
	print(f"Allow: {methods}")
	print()

def updateJSON():
	file = open("school.json", "w")
	json.dump(data, file, indent=2)
	file.close()

def main():

	students = data["students"]
	courses = data["courses"]

	if dest == None:
		status404()

	elif dest[0] == "students":

		for student in students:
			student["link"] = url

		if len(dest) == 1:
			if request == "GET":
				status200()

				for student in students:
					student["link"] += "/" + str(student["id"])

				print(json.dumps(students, indent=2))

			elif request == "POST":
				new_student = sys.stdin.read()
				try:
					new_student_JSON = json.loads(new_student)
				except:
					status400(message="Invalid format")
					return

				new_student_JSON["courses"] = []

				keys = new_student_JSON.keys()

				if len(keys) != 2 or "id" not in keys or "name" not in keys:
					status400(2, 'id,name')

				elif not isinstance(new_student_JSON["id"], int):
					status400('id', 'int')

				elif not isinstance(new_student_JSON["name"], str):
					status400('name', 'string')

				else:
					unique_student = True

					for student in students:
						if student["id"] == new_student_JSON["id"]:
							unique_student = False

					if unique_student:
						status303()

						students.append(new_student_JSON)
						updateJSON()

			else:
				status405("GET,POST")

		else:
			try:
				id = int(dest[1])

			except:
				status400(message='The ID of the record is not an integer')
				return

			else:
				s = None
				for student in students:
					if student["id"] == id:
						s = student

			if s == None:
				status404()

			if len(dest) == 2:
				if request == "GET":
					status200()

					print(json.dumps(s, indent=2))

				elif request == "PUT":
					new_name = sys.stdin.read()
					new_name_JSON = json.loads(new_name)

					keys = new_name_JSON.keys()

					if len(keys) != 1 or keys[0] != "name":
						status400(1, 'name')

					elif not isinstance(new_name_JSON["name"], str):
						status400("name", "string")

					else:
						status303()
						s.update(new_name_JSON)

						updateJSON()

				elif request == "DELETE":
					status303()

					new_students = []
					for student in students:
						if student["id"] != id:
							new_students.append(student)

					data["students"] = new_students

					updateJSON()

				else:
					status405("GET,PUT,DELETE")

			elif len(dest) == 3:
				if request == "POST":
					new_course = sys.stdin.read()
					try:
						new_course_JSON = json.loads(new_course)
					except:
						status400(message="Invalid format")
						return

					unique_course = True
					existing_course = False

					for course in s["courses"]:
						if course == new_course_JSON:
							unique_course = False

					for course in courses:
						if course["id"] == new_course_JSON:
							existing_course = True

					if not existing_course:
						status400(message='This course does not exist')

					if not unique_course:
						status400(message='The student already has this course')

					elif unique_course and existing_course:
						status303()

						s["courses"].append(new_course_JSON)
						updateJSON()

				else:
					status405("POST")

	elif dest[0] == "courses":

		for course in courses:
			course["link"] = url

		if len(dest) == 1:
			if request == "GET":
				status200()

				for course in courses:
					course["link"] += "/" + course["id"]

				print(json.dumps(courses, indent=2))

			elif request == "POST":
				new_course = sys.stdin.read()
				try:
					new_course_JSON = json.loads(new_course)
				except:
					status400(message="Invalid format")
					return

				keys = new_course_JSON.keys()

				if len(keys) != 1 or keys[0] != "id":
					status400(1, 'id')

				elif not isinstance(new_course_JSON["id"], str):
					status400('id', 'string')

				else:
					unique_course = True

					for course in courses:
						if course["id"] == new_course_JSON["id"]:
							unique_course = False

					if unique_course:
						status303()

						courses.append(new_course_JSON)
						updateJSON()

					else:
						status400(message='The course ID already exists')

			else:
				status405("GET,POST")

		elif len(dest) == 2:
			id = dest[1]
			c = None
			for course in courses:
				if course["id"] == id:
					c = course

			if c == None:
				status404()

			elif request == "GET":
				status200()

				print(json.dumps(c, indent=2))

			elif request == "DELETE":
				status303()

				empty_class = True

				for student in students:
					if c["id"] in student["courses"]:
						empty_class = False

				if empty_class:
					courses.remove(c)

					updateJSON()

				else:
					status400(message="This class is not empty and cannot be deleted")

			else:
				status405("GET,DELETE")

	elif dest[0] == "debug":
		if request == "GET":
			status200()

			print(json.dumps(data, indent=2))

		else:
			status405("GET")

try:
	main()
except:
	print("Status: 500 Internal Server Error")
	print("Content-Type: text/html")
	print()