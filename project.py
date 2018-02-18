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
import datetime
import time
import subprocess

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

### Function that reads info from scan_params.txt ###
def scan_params():
	try:
		# Try to open file for reading
		scan_file = open("scan_params.txt", "r")

		# Starting with the beginning of the file
		scan_file.seek(0)

		# Reading the line
		scan = scan_file.read().splitlines()

		# CLosing the file
		scan_file.close()
	except IOError:
		return []
	scan_info=[]
	for data in scan:
		print(data)
		scan_info.append(data.split(":"))
	return scan_info

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

### Function which is checking which addresses are available to ping ###
def pingy(ip_list):
	ip_available = []
	for ip in ip_list:
		ping_reply = subprocess.call(['ping', '-c', '2', '-w', '2', '-q', '-n', str(ip)])
		### Appending ip to list if device is pingable ###
		if ping_reply == 0:
			ip_available.append(ip)
	#print(ip_available)
	return ip_available

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
	# For later - here need to be checked if database is
	scan = scan_params()
	print(scan)
	if len(scan)!=0:
		empty = False
	else:
		empty=True
	path = os.path.dirname(os.path.realpath(__file__))+"\ip_range.txt\n"
	path_pass = os.path.dirname(os.path.realpath(__file__)) + "\passwords.txt\n"
	form=Start()
	if form.validate_on_submit():
		ip_list=ip_range()
		password_list=passwords()
		ip_available = pingy(ip_list)
		if len(ip_available)==0:
			flash("No ability to ping any device with given IP adress. Check IP addresses in file and try again. ")
		else:
			flash("Ability to connect with devices in the network. Trying to establish ssh session in order to gather information. ")
	return render_template("index.html",empty=empty, form=form, path=path, path_pass=path_pass,scan_params=scan,id="R1")

### shutdown route - closing web server ###
@app.route("/shutdown")
def shutdown():
	shutdown_server()
	return render_template("shutting.html")


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
