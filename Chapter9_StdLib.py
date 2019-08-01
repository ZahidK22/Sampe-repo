import csv
import json
import math
import os
import random
import shutil
import smtplib
import sqlite3
import string
import subprocess
import sys
import time
import webbrowser
from datetime import datetime, timedelta
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from string import Template
from time import ctime
from zipfile import ZipFile

import requests

# 9.2 - WORKING WITH PATHS

"""Path(r"C:\Program Files\Microsoft")
# To avoid the escape sequence that makes it look ugly
Path(r"C:\Program Files\Microsoft") # r is the raw string so no need for //
Path() # represents current folder
Path("ecommerce/__init__.py") # current folder + ecommerce + __init__.py
Path() / Path("ecommerce") #combining two path objects
Path() / "ecommerce" / "__init__.py" # combining path object with a string
Path.home() #returns home directory of the path user """

# current folder + ecommerce + __init__.py
"""path = Path("ecommerce/__init__.py")
path.exists()  # to check if file/directory exists
path.is_file()  # to check if the path represents a file or not
path.is_dir()
# extract info from the path object #outputs __init__.py - returns only file name
print(path.name)
print(path.stem)  # return file name without the extension .py - outputs __init__
print(path.suffix)  # to get extension .py - return .py
print(path.parent)  # get the parent file - outputs ecommerce
"""
# NONE OF THIS RENAMEES THE FILES

# # To create a new path object based on this existing path but only change the name and the extension of the file
# path1 = path.with_name("file.txt")
# print(path)  # returns ecommerce\ file.txt
# # outputs - c:\Users\omanz\Documents\python\python trials\PythonWithMosh\ecommerce\__init__.py
# print(path.absolute())
# # c:\Users\omanz\Documents\python\python trials\PythonWithMosh\ecommerce\ file.txt - file doesnt exist yet. only representing its path
# print(path1.absolute())
# # print(path.with_suffix(".txt")) #change extension of file ecommerce\__init__.txt


# 9.3 - WORKING WITH DIRECTORIES
"""path = Path("ecommerce")  # this is a path object that represents a directory
path.exists()  # returns boolean
path.mkdir()  # to create a directory
path.rmdir()  # to remove a directory
path.rename("ecommerce2")  # renaming the directory"""

# To get the list of files and directories in this path
"""path = Path("ecommerce")"""
# outputs <generator object Path.iterdir at 0x00DA96F0> - returns a new value everytime we iterate
# not stored in memory
"""
print(path.iterdir())
for p in path.iterdir():
    print(p) """

# if the no. of directories are small we can use list comprehension
# outputs - [WindowsPath('ecommerce/customer'), WindowsPath('ecommerce/shopping'),
#  WindowsPath('ecommerce/__init__.py'), WindowsPath('ecommerce/__pycache__')]
# The path class imported in the top is the base class for two different classes , PoxisPath and WindowsPath
"""paths = [p for p in path.iterdir()]
print(paths)"""
# To get only directories - [WindowsPath('ecommerce/customer'), WindowsPath('ecommerce/shopping'), WindowsPath('ecommerce/__pycache__')]
"""paths = [p for p in path.iterdir() if p.is_dir()]
print(paths)"""
# two limitations of iterdir():
# cannot search by the pattern
# doesnt search recursively

# this method takes a pattern - # search for all files input "*.*"
# [WindowsPath('ecommerce/__init__.py')]
"""py_files = [p for p in path.glob("*.py")]
print(py_files)"""
# To search recursively
# Outputs - [WindowsPath('ecommerce/__init__.py'), WindowsPath('ecommerce/customer/contact.py'),
# WindowsPath('ecommerce/customer/__init__.py'), WindowsPath('ecommerce/shopping/sales.py'),
# WindowsPath('ecommerce/shopping/__init__.py')]
"""py_files = [p for p in path.glob("**/*.py")]
print(py_files)"""
# the other option is to use the r glob method - which stands for recursive glob
"""py_files = [p for p in path.rglob("*.py")]
print(py_files)"""


# 9.4 - WORKING WITH FILES
# path = Path("ecommerce/__init__.py")
"""path.exists()
path.rename("__init__.txt")
path.unlink() # detete the file """

# return info on the file - os.stat_result(st_mode=33206, st_ino=7599824371689976, st_dev=2993566424,
#  st_nlink=1, st_uid=0, st_gid=0, st_size=233, st_atime=1564230851, st_mtime=1564235566, st_ctime=1564230851)
# st_size returns size of file in bytess, last access time(st_attime), last modified time(st_mtime), creation time(st_ctime)
# to see readable time - since this gives the epic time - time of start of the computer
# using from time import ctime
"""print(path.stat())
# outputs Sat Jul 27 16:34:11 2019 - creation time of this file
print(ctime(path.stat().st_ctime))
# returns content of the file as bytes object when representing binary data
path.read_bytes()"""

# using read text is better than with open("__init__.py","r") as file:
"""print(path.read_text()) """  # returns the content of the file as a string
# path.write_text("...") or path.write_bytes("") all these methods take care of opeinng and closing of the file

# the path object is not the ideal to copy a file
"""source = Path("ecommerce/__init__.py")
target = Path() / "__init__.py"
target.write_text(source.read_text())"""  # a little bit tedious

# using module shell utilities as shutil as it moves methods for copying and moving directories
"""shutil.copy(source, target) # copies source to target """


# 9.5 - WORKING WITH ZIP FILES
# importing zipfile class
# creating ZipFile object and create this file in our current folder
# want to get everything in the ecommerce file into the zip file
"""with ZipFile("files.zip", "w") as zip:
    for path in Path("ecommerce").rglob("*.*"):
        zip.write(path)"""
# zip.close() use with as statement
# Reading the Zip file
"""with ZipFile("files.zip") as zip:
    print(zip.namelist())
    info = zip.getinfo("ecommerce/__init__.py")
    print(info.file_size)  # 233
    # 233 - no compression because we are dealing with a really simple file
    print(info.compress_size)
    # optionally specify a directory to extract the compressed zip file into
    zip.extractall("extract")

"""

# 9.6 - WORKING WITH CSV FILES - COMMA SEPARATED VALUE
# import csv - csv is a simplified spreadsheet stored in a plain text file
"""with open("data.csv", 'w') as file:
    writer = csv.writer(file)  # 1st parameter is a file object
    writer.writerow(["transcation_id", "product_id", "price"])
    writer.writerow([1000, 1, 5])
    writer.writerow([1000, 2, 15])"""

# Want to read the file
"""with open("data.csv") as file:
    reader = csv.reader(file)"""
# print(list(reader))
# output - [['transcation_id', 'product_id', 'price'], [], ['1000', '1', '5'], [], ['1000', '2', '15'], []]
# each line in csv file is a list of objects, valur of each cell is represented as a string
"""for row in reader:
        print(row)"""  # no output
# at line 143 the reader or object has an index or position at the beginning of the file
# when converting the reader to a list that position is converted to the end of the file
# so when iterating we are at the end of the file

# 9.7 - WORKING WITH JSON FILES
# JSON - Javascript Objecti Notation
# Popular way to format data in a human readable way
# import json
"""movies = [
    {"id": 1, "title": "Terminator", "year": 1989},
    {"id": 2, "title": "Kindergarden cop", "year": 1993}
]

data = json.dumps(movies)"""  # gets a string of movies data formatted as json
# [{"id": 1, "title": "Terminator", "year": 1989}, {"id": 2, "title": "Kindergarden cop", "year": 1993}]
"""print(data)"""
# writing to a file so call path class from pathlib
"""Path("moves.json").write_text(data)"""

# Reading json data
"""data = Path("moves.json").read_text()"""
# parse string into an array of objects
"""movies = json.loads(data)"""
# [{'id': 1, 'title': 'Terminator', 'year': 1989}, {'id': 2, 'title': 'Kindergarden cop', 'year': 1993}]
"""print(movies)
print(movies[0]["title"])"""  # Outputs - Terminator

# 9.8 - WORKING WITH SQLite DataBase
# SQLite is a light DataBase used for storiing data on an application
# Often used for small applications that we run on phones and tablets
# Allows us to easily store data in a structure format with a table of rows and columns
# import sqlite3
# reading all the data from moves.json file and storing them in SQLite database
# import json and path class
# making the list of dictionaries parsed
"""movies = json.loads(Path("moves.json").read_text())"""
# print(movies) #[{'id': 1, 'title': 'Terminator', 'year': 1989}, {'id': 2, 'title': 'Kindergarden cop', 'year': 1993}]

# storing the list in a database (if not available python will create it for us) - returning a connection object
# connection = sqlite3.connect("db.sqlite3") - connection object should be closed when done
# need to create a command that is the instruction to the database to create,update and delete data etc.
# ? are placeholders for the values of id, title and year

"""with sqlite3.connect("db.sqlite3") as connection:
    command = "INSERT INTO Movies VALUES(?,?,?)"
    for movie in movies:
        connection.execute(command, tuple(movie.values()))
    connection.commit()"""
# Get error sqlite3.OperationalError: no such table: Movies because we are dealing with an empty database as it has no tables
# IN SQL  - Id is set as PK - Primary Key which is a unique identifier of each movie
# IN SQL - Not box is stating that the data in these columns cannot be null
# Data is now updated in the SQL Database

# Reading from SQL Database
'''with sqlite3.connect("db.sqlite3") as connection:
    command = "SELECT * FROM Movies"'''  # Selecting all Movies
# this gives a cursor, which is an iterable object
"""
    cursor = connection.execute(command)
    for row in cursor:
        print(row)"""
# Returns all the rows in this table in one go not using the for loop cuz we will be at the end of the file
# Outputs [(1, 'Terminator', 1989), (2, 'Kindergarden cop', 1993)]
"""movies = cursor.fetchall()
    print(movies)"""
# outputs:(1, 'Terminator', 1989)
# (2, 'Kindergarden cop', 1993)

# 9.9 - WORKING WITH TIMESTAMPS
# two modules time and datetime(year, month)
# import time
"""print(time.time())"""  # returns current date time -
# output 1564478425.0976913 - represents no. of seconds from the beginning of time of the operating system
# Referred as unix epic time


"""def send_emails():
    for i in range(10000):
        pass


start = time.time()
send_emails()
end = time.time()
duration = end - start
print(duration)"""  # 0.0009970664978027344 TIME IT TOOK TO EXECUTE

# 9.10 - WORKING WITH DATETIME OBJECTS
# from datetime import datetime
# import datetime
# one way of creating a datetime object - too long
# dt = datetime.datetime(2019,1,1)
"""dt1 = datetime(2019, 1, 1)
dt2 = datetime.now()  # current datetime 2019-07-30 13:28:30.369338
print(dt2 > dt1) """  # Prints True
# Parsing or converting from a date time string to datetime object with directives %Y to let python know what is year, month etc.
"""dt = datetime.strptime("2019/01/01", "%Y/%m/%d")"""

# Convert timestamp to a datetime object - import time module
# time.time()
"""dt = datetime.fromtimestamp(time.time())
print(dt)  # 2019-07-30 13:36:58.975776
print(f'{dt.year}/{dt.month}')"""  # 2019/7

# method for formatting datetimes - to convert datetime object to string
"""print(dt.strftime("%Y/%m"))"""  # 2019/07


# 9.11 - WORKING WITH TIME DELTAS
# from datetime import datetime
# from datetime import timedelta, represents a duration
# only has days, seconds and microseconds, months and years are varying amount of times
"""
dt1 = datetime(2019, 1, 1)
dt2 = datetime.now()
duration = dt2 - dt1
print(duration)  # 210 days, 15:02:47.149194
print("days", duration.days)
print("seconds", duration.seconds)  # seconds 54289
# 18198578.722349 = no.of seconds in days + 54289
print("total seconds:", duration.total_seconds())"""

# Add timedelta object to a datetime object
"""dt1 = datetime(2019, 1, 1) + timedelta(days=1, seconds=1000)
print(dt1)  # 2019-01-02 00:16:40 - adding 1 day and 1000 sec
dt2 = datetime.now()"""


# 9.12 - GENERATING RANDOM VALUES
# import random
"""print(random.random())  # Generate random value between 0 and 1
print(random.randint(1, 10))  # Generate random integer
# Randomly picks one of the items in this array
print(random.choice([1, 2, 3, 4]))
print(random.choices([1, 2, 3, 4], k=2))"""  # pick 2 choices out of 4


# Generate a random password
"""print("".join(random.choices("abcdefghi", k=4))) """  # picking 4 items


# import string
# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ also includes string.digits, string.lowercase etc
# print(string.ascii_letters)
# need to include all alphabets, numerical values etc... but too long so import string
"""print("".join(random.choices(string.ascii_letters + string.digits, k=4)))"""  # v6Qd

# Shuffling an array
"""numbers = [1, 2, 3, 4]
random.shuffle(numbers) # changes the order  randomly of numbers array
print(numbers)"""  # [3, 2, 4, 1]

# 9.13 - OPENING THE BROWSER
# Particularly useful if you are building an automation script that does some tasks and then opens are browser window
# Ex: build your website locally on your machine and when you're done, you run the script to get deployed to a web server
# At the end you will have open a browser window and type the address of your website and press enter
# This can all be automated so we can have the python script open up at the end of deployment
# import webbrowser
"""
print("Deployment completed")
webbrowser.open("http://www.google.com")"""

# 9.14 - SENDING EMAILS
# Useful if you have a database of customers and send them emails based on their interests
# MIME  - Multipurpose Internet Mail Extension - Standard that defines the fomrat of email messages
# With an instance of this class we can send an email message that includes both html and plain text if the email client supports either
# from email.mime.multipart import MIMEMultipart

# Creating Template object for 9.15 for html email sending
# Read text return the entire content of the file as a string
"""template = Template(Path("template.html").read_text())"""
# template.substitute() - replace dynamically

"""message = MIMEMultipart()"""


# Setting various headers supported by MIMEMultipart objects
# No header called body so we use the method attach
"""
message["from"] = "Zahid Kamil"
message["to"] = "zahid.kamil1573@gmail.com"
message["subject"] = "Python With Mosh"
"""

# from email.mime.text import MIMEText
# By default 2nd para is set to plain text but you can set it to html as "html"
# message.attach(MIMEText("Body"))
"""# body = template.substitute({"name": "John"})  # Values to replace dynamically
body = template.substitute(name="John") # Alternatively, we can use key-word arguments 
message.attach(MIMEText(body, "html"))
"""

# Attaching image
"""# from email.mime.image import MIMEImage"""
# need to pass image data in binary so we need to import path class using pathlib
"""message.attach(MIMEImage(Path("Picture1.jpg").read_bytes()))"""

# We need to send it using an smtp server
# import smtplib
# Values depend on the smtp server we use and this returns an smtp object
"""with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()  # a hello message greeting to the smtp server as this is part of the smtp protocol
    smtp.starttls()  # puts the smtp connection in tls mode - Transport Layer Security, so with this all the commands we sent to smtp server will be encrypted
    smtp.login("JackSparrow.88922", "coolBoy22$")
    smtp.send_message(message)
    print("Sent...")"""


# 9.15 - WORKING WITH TEMPLATES
# Creating html templates in python use create websites
# $name - to define a parameter so that we can replace with the recipients name
# from string import Template
# We use the template class to replace the parameters in the template string


# 9.16 - COMMAND-LINE ARGUMENTS
# Create python programmme that expects comman-like arguments
# argv - argument variables
# import sys
"""print(sys.argv)"""

# In terminal python Chapter9_StdLib.py -a -b -c
# ['Chapter9_StdLib.py', '-a', '-b', '-c'] - first item is the python script
# Check if the user has supplied any arguments if len ==1
"""if len(sys.argv) == 1:
    print("USAGE: Python3 Chapter9_StdLib.py <password>")
else:
    password = sys.argv[1]
    print("Password",password)"""


# 9.17 - RUNNING EXTERNAL PROGRAMS
# How to call external programs from python scripts
# Useful in automation scripts
# LEarn operating system commands as well as external programs
# Ex: Python script execute another python script
# import subprocess - can spot a child process
# A process is an instance of a running program so with this module we can run other programs

# All these methods are helper methods to create an instance of the p open class (process open)
# However, these a old methods and there is a newer method
"""subprocess.call
subprocess.check_call
subprocess.check_output
"""

# Newer method
# subprocess.run(["dir",r"/s",shell=True])
# subprocess.run(["cmd", "/c", "dir"])

# import os
# os.system('dir')

'''
r = requests.get("https://www.google.com")
print(r.status_code)  # thidhifrijdsijsif

print("this is cool!")'''
# To install virtual environment type python -m venv venv_module_name
