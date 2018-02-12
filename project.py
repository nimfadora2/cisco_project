### Network management tool ###

### importing necessary modules for creating website ####
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
from forms import IpRange

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
		raise RunTimeError('Not running with the Werkzeug Server')
	func()

### Function that reads valid ip range from file ###
def ip_range():
	check = False
	try:
		# Try to open file for reading
		ip_file = open("ip_range.txt","r")
		
		# Starting with the beginning of the file
		ip_file.seek(0)
		
		# Reading the line
		ip_list = ip_file.readlines()

		# CLosing the file
		ip_file.close()
	except IOError:
		#flash("The file does not exist! Please check and try again!")
		return redirect(url_for("main"))
	flash("It is ok!")
	return redirect(url_for("main"))

############################
### Routes in web server ###
############################

# In this part there are routes for web server - data in decorators
# e.g. @app.route("/shutdown") show the end of page we should write 
# to have access to this part of code, e.g. 127.0.0.1:5000/shutdown
# in the mentioned case.

### main route - displaying necessary information ###
@app.route("/")
def main():
	# For later - here need to be checked if database is filled
	empty = True
	if empty==True:
		ip_range()
	return render_template("index.html",empty=empty)


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

'''
