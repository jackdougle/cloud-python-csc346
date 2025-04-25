#!/usr/bin/python3

# Assumes the school database is already created in SQL server online or locally

import cgitb
import os
import json
import sys
import MySQLdb
from info import HOST, USER, PASS, NAME

cgitb.enable()

conn = MySQLdb.connect(
	host=HOST,
	user=USER,
	passwd=PASS,
        db=NAME
)

cursor = conn.cursor()

request = os.environ.get("REQUEST_METHOD")
url = os.environ.get("HTTP_HOST") + os.environ.get("SCRIPT_NAME")
dir = os.environ.get("PATH_INFO")
dest = dir[1:].split("/") if dir else None

def status200():
        print("Status: 200 OK")
        print("Content-Type: application/json\n")

def status303():
        print("Status: 303 Redirect")
        print("Location: " + url + "\n")

def status400(para=None, type=None, message=None):
        print("Status: 400 Bad Request")
        print("Content-Type: text/html\n")
        print("<html><body><p>400 Bad Request</p>")
        if message:
                print("<p>" + message + "</p>")
        elif isinstance(para, int):
                print("<p>" + request + " to " + dir + " must have exactly " + str(para) + " field(s): " + type + "</p>")
        elif para and type:
                print("<p>The " + para + " parameter must be a(n) " + type + "</p>")
        print("</body></html>")

def status404():
        print("Status: 404 Not Found")
        print("Content-Type: text/html\n")
        print("<html><body><p>Page not found, check URL</p><p>PATH_INFO: " + str(dir) + "</p></body></html>")

def status405(methods):
        print("Status: 405 Method Not Allowed")
        print("Allow: " + methods + "\n")

def main():
        global url

        if dest is None:
                status404()
                return

        if dest[0] == "students":

                if len(dest) == 1:
                        if request == "GET":
                                status200()

                                cursor.execute("SELECT * FROM students")
                                raw_data = cursor.fetchall()

                                students = []
                                for row in raw_data:
                                        student = {}
                                        student["id"] = row[0]
                                        student["name"] = row[1]
                                        student["link"] = url + "/" + str(student["id"])
                                        students.append(student)

                                print(json.dumps(students, indent=2))

                        elif request == "POST":
                                try:
                                        new_student = json.loads(sys.stdin.read())
                                except:
                                        status400(message="Invalid format")
                                        return

                                if set(new_student.keys()) != {"id", "name"}:
                                        status400(2, 'id,name')
                                        return

                                if not isinstance(new_student["id"], int):
                                        status400('id', 'int')
                                        return

                                if not isinstance(new_student["name"], str):
                                        status400('name', 'string')
                                        return

                                cursor.execute("SELECT id FROM students WHERE id = %s", (new_student["id"],))

                                if cursor.fetchone():
                                        status400(message="Student ID already exists")
                                else:
                                        cursor.execute("INSERT INTO students (id, name) VALUES (%s, %s)", (new_student["id"], new_student["name"]))
                                        conn.commit()
                                        status303()

                        else:
                                status405("GET,POST")

                else:
                        try:
                                studentID = int(dest[1])
                        except:
                                status400(message="The ID of the record is not an integer")
                                return

                        cursor.execute("SELECT * FROM students WHERE id = %s", (studentID,))

                        if cursor.fetchall() is None:
                                status404()
                                return

                        student = {}
                        student["id"] = row[0]
                        student["name"] = row[1]

                        if len(dest) == 2:
                                if request == "GET":
                                        status200()
                                        student["link"] = url + "/" + str(student["id"])
                                        cursor.execute("SELECT courseID FROM registrations WHERE studentID = %s", (studentID,))
                                        courses = []
                                        for c_row in cursor.fetchall():
                                                courses.append(c_row[0])
                                        student["courses"] = courses
                                        print(json.dumps(student, indent=2))

                                elif request == "PUT":
                                        try:
                                                new_name = json.loads(sys.stdin.read())
                                        except:
                                                status400(message="Invalid format")
                                                return

                                        if list(new_name.keys()) != ["name"] or not isinstance(new_name["name"], str):
                                                status400(1, 'name')
                                                return

                                        cursor.execute("UPDATE students SET name = %s WHERE id = %s", (new_name["name"], studentID))
                                        conn.commit()
                                        status303()

                                elif request == "DELETE":
                                        cursor.execute("DELETE FROM students WHERE id = %s", (studentID,))
                                        conn.commit()
                                        status303()

                                else:
                                        status405("GET,PUT,DELETE")

                        elif len(dest) == 3:
                                if request == "POST":
                                        try:
                                                new_courseID = json.loads(sys.stdin.read())
                                        except:
                                                status400(message="Invalid format")
                                                return

                                        cursor.execute("SELECT id FROM courses WHERE id = %s", (new_courseID,))
                                        if cursor.fetchone() is None:
                                                status400(message="This course does not exist")
                                                return

                                        cursor.execute("SELECT * FROM registrations WHERE studentID = %s AND courseID = %s", (studentID, new_courseID))
                                        if cursor.fetchone():
                                                status400(message="The student already has this course")
                                                return

                                        cursor.execute("INSERT INTO registrations (studentID, courseID) VALUES (%s, %s)", (studentID, new_courseID))
                                        conn.commit()
                                        status303()

                                else:
                                        status405("POST")

        elif dest[0] == "courses":

                if len(dest) == 1:
                        if request == "GET":
                                status200()
                                cursor.execute("SELECT id FROM courses")
                                raw_data = cursor.fetchall()
                                courses = []
                                for row in raw_data:
                                        course = {}
                                        course["id"] = row[0]
                                        course["link"] = url + "/" + course["id"]
                                        courses.append(course)
                                print(json.dumps(courses, indent=2))

                        elif request == "POST":
                                try:
                                        new_course = json.loads(sys.stdin.read())
                                except:
                                        status400(message="Invalid format")
                                        return

                                if list(new_course.keys()) != ["id"] or not isinstance(new_course["id"], str):
                                        status400(1, 'id')
                                        return

                                cursor.execute("SELECT id FROM courses WHERE id = %s", (new_course["id"],))
                                if cursor.fetchone():
                                        status400(message="The course ID already exists")
                                else:
                                        cursor.execute("INSERT INTO courses (id) VALUES (%s)", (new_course["id"],))
                                        conn.commit()
                                        status303()

                        else:
                                status405("GET,POST")

                elif len(dest) == 2:
                        courseID = dest[1]
                        cursor.execute("SELECT id FROM courses WHERE id = %s", (courseID,))
                        row = cursor.fetchone()

                        if row is None:
                                status404()
                                return

                        course = {}
                        course["id"] = row[0]
                        course["link"] = url + "/" + course["id"]

                        if request == "GET":
                                status200()
                                print(json.dumps(course, indent=2))

                        elif request == "DELETE":
                                cursor.execute("SELECT * FROM registrations WHERE courseID = %s", (courseID,))
                                if cursor.fetchone():
                                        status400(message="This class is not empty and cannot be deleted")
                                else:
                                        cursor.execute("DELETE FROM courses WHERE id = %s", (courseID,))
                                        conn.commit()
                                        status303()

                        else:
                                status405("GET,DELETE")

        elif dest[0] == "debug" and request == "GET":
                status200()

                cursor.execute("SELECT * FROM students")
                student_rows = cursor.fetchall()
                students = []
                for s_row in student_rows:
                        student = {}
                        student["id"] = s_row[0]
                        student["name"] = s_row[1]
                        cursor.execute("SELECT courseID FROM registrations WHERE studentID = %s", (s_row[0],))
                        courses = []
                        for c_row in cursor.fetchall():
                                courses.append(c_row[0])
                        student["courses"] = courses
                        students.append(student)

                cursor.execute("SELECT id FROM courses")
                course_rows = cursor.fetchall()
                courses = []
                for c_row in course_rows:
                        course = {}
                        course["id"] = c_row[0]
                        courses.append(course)

                output = {
                        "students": students,
                        "courses": courses
                }

                print(json.dumps(output, indent=2))

        else:
                status405("GET")

try:
        main()
except Exception:
        print("Status: 500 Internal Server Error")
        print("Content-Type: text/html")
        print()
finally:
        cursor.close()
        conn.close()