### Network management tool ###
### Group 8, Cisco Engineer Incubator 5.0 ###

### To do: ###
# 1. Check if the addresses in file are appropriate
# 2. Change the main when all data is gathered

### importing necessary modules for creating website ####
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
from forms import Start
import ipaddress
import threading
import time

########################################
### Initialization of needed modules ###
########################################

# Web server and extensions, such as SQL database need
# initialization - this is part where it takes place.

### application initialization to start webserver ####
app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

#############################################
### Function definitions used in webpages ###
#############################################

# To make part with decorators smaller functions are separated
# from web server.

### Function responsible for shutting server down ###
def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()

### Function that reads valid ip range from file ###
def ip_range():
	try:
		# Try to open file for reading
		ip_file = open("ip_range.txt","r")
		
		# Starting with the beginning of the file
		ip_file.seek(0)
		
		# Reading the line
		ip_list_prev = ip_file.read()

		# CLosing the file
		ip_file.close()
	except IOError:
		flash("The file 'ip_range.txt' does not exist! Please check and try again!")
		return None
	### Reading into list IP's delimited by "," ###
	ip_list_prev=ip_list_prev.split(",")

	ip_list=[]
	### Striping each IP of excess white spaces ###
	for i in range(len(ip_list_prev)):
		ip_list_prev[i]=ip_list_prev[i].strip()

		### Checking if adddressess are valid - if so apppending them to ip_list, else - returning []
		if "#" in ip_list_prev[i]:
			temp = ip_list_prev[i].split("#")
			ip_temp = temp[0]
			number = int(temp[1])
			try:
				ip=ipaddress.ip_address(ip_temp)
				ip_list.append(ip)
			except ValueError:
				flash("Invalid IP address! Check and try again.")
				ip_list = []
				return None
			for i in range(1,number):
				ip_list.append(ip+i)
		else:
			try:
				ip_list.append(ipaddress.ip_address(ip_list_prev[i]))
			except ValueError:
				flash("Invalid IP address! Check and try again.")
				return None
	flash("The file ip_range.txt has been read.")
	return ip_list

### Function that reads passwords and from file and puts them in the list ###
def passwords():
	try:
		# Try to open file for reading
		passwords_file = open("passwords.txt", "r")

		# Starting with the beginning of the file
		passwords_file.seek(0)

		# Reading the line
		password = passwords_file.read()

		# CLosing the file
		passwords_file.close()
	except IOError:
		flash("The file 'passwords.txt' does not exist! Please check and start the process again!")
		return None
	flash("The file passwords.txt has been read.")
	return password

### Function responsible for checking if there is ability to ping the host, connecting to them and collecting information ###
def pingy(ip_list,passwords):
	return True

############################
### Routes in web server ###
############################

# In this part there are routes for web server - data in decorators
# e.g. @app.route("/shutdown") show the end of page we should write 
# to have access to this part of code, e.g. 127.0.0.1:5000/shutdown
# in the mentioned case.

### main route - displaying necessary information ###
@app.route("/", methods=["GET","POST"])
def main():
	# For later - here need to be checked if database is filled
	empty = True
	path = os.path.dirname(os.path.realpath(__file__))+"\ip_range.txt\n"
	path_pass = os.path.dirname(os.path.realpath(__file__)) + "\passwords.txt\n"
	form=Start()
	if form.validate_on_submit():
		ip_list=ip_range()
		password_list=passwords()
		data = pingy(ip_list,passwords)
	return render_template("index.html",empty=empty, form=form, path=path, path_pass=path_pass)

### shutdown route - closing web server ###
@app.route("/shutdown")
def shutdown():
	shutdown_server()
	return "Shutting server down..."


### run application ###
# This application is placed in loopback 127.0.0.1 at the port 5000.
# This can be changed if needed.
if __name__=='__main__':
	app.run(debug=True)

#######################
### Sources of help ###
#######################
'''
flask.pocoo.org/snippets/67/
https://docs.python.org/3/library/ipaddress.html
Book: M. Ginberg Flask Web Development
'''
