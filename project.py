### Network management tool ###
### Group 8, Cisco Engineer Incubator 5.0 ###
### Authors: Anna Luszczkiewicz, Kinga Slowik, Volodymyr Ushnevych ###

### importing necessary modules for creating website ####
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
import os
from forms import Start
import ipaddress
import datetime
import time
import subprocess
import os.path
import re
import matplotlib as plt
import networkx as nx

########################################
### Initialization of needed modules ###
########################################

# Web server and extensions, such as SQL database need
# initialization - this is part where it takes place.

### application initialization to start webserver ####
app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)

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
	done_well=False
	for data in scan:
		scan_info.append(data.split(":",1))
		if data.split(":")[0]=="Date of last successfull scan":
			done_well=True
	return scan_info,done_well

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
	ip_list_prev=ip_list_prev.strip().strip(",").split(",")
	ip_list=[]
	### Striping each IP of excess white spaces ###
	for i in range(len(ip_list_prev)):
		if ip_list_prev[i]==[]: continue
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
				return ip_list
			for i in range(1,number):
				ip_list.append(ip+i)
		else:
			try:
				ip_list.append(ipaddress.ip_address(ip_list_prev[i]))
			except ValueError:
				flash("Invalid IP address! Check and try again.")
				return ip_list
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

### Function for reading file output to prepare it to the website format ###
def formatting():
	### Reading file output ###
	output = open("final.txt", "r")
	out = output.read().splitlines()
	output.close()

	all = []
	number = 0
	current = []
	k=0
	### State machine for appropriate reading of file ###
	for line in out:
		k=k+1
		### Empty line - separator for routers ###
		if line == '':
			if current != []:
				current.append(modules)
				all.append(current)
			current = []
			number = 0
		### Start of reading - line with field names ###
		### Used for general info ###
		elif line.startswith("Name"):
			number = 0
			prev = line.split('    ')
		elif number == 0:
			temp = line.split('    ')
			general = []
			for i in range(len(prev)):
				general.append([prev[i], temp[i]])
			number = 1
			current.append(temp[0])
		elif number == 1:
			temp = line.split(":")
			general.append([temp[0], temp[1].strip()])
			current.append(general)
			number = 2
			interfaces = []
		### Lines with names and status of interfaces ###
		elif number == 2:
			names = re.split(r'\s+', line.strip())
			if line == "Inventory of device:":
				current.append(interfaces)
				modules = []
				modules.append(['Name', 'Description'])
				number = 3
			elif len(names) == 5 and names[1] == 'IP':
				names[1:3] = [' '.join(names[1:3])]
				interfaces.append(names[0:4])
			elif len(names) == 4:
				interfaces.append(names)
			else:
				names[2:4] = [' '.join(names[2:4])]
				interfaces.append(names[0:4])
		### Part responsible for adding modules ###
		elif number == 3:
			temp = line.split("\", ")
			modules.append([temp[0].strip('NAME: ').strip("\""), temp[1].strip('DESCR: ').strip("\"")])
			if k==len(out):
				current.append(modules)
				all.append(current)
	return all

### Function for keeping scan parametres ###
def scan_parametres(ok,scan,person):

	### Writing to file if it is empty or not existing ###
	if scan==[]:
		out = open("scan_params.txt","w")
		### Writing data if everything went successful ###
		if ok==False:
			out.write("Date of last unsuccessfull scan: "+str(datetime.date.today())+"\n")
			out.write("Hour of last unsuccessfull scan: "+str(datetime.datetime.now().time())+"\n")
			out.write("Person responsible: "+person+"\n")
		### Writing data if scan went unsuccessful ###
		else:
			out.write("Date of last successfull scan: "+str(datetime.date.today())+"\n")
			out.write("Hour of last successfull scan: "+str(datetime.datetime.now().time())+"\n")
			out.write("Person responsible: "+person+"\n")
		out.close()
	### Writing data to already existing file ###
	else:
		out = open("scan_params.txt","r")
		out_data = out.read().splitlines()
		out.close()
		success=False
		fail=False
		### Reading file ###
		for i in range(len(out_data)):
			out_data[i]=out_data[i].strip().split(":",1)
			out_data[i][0]=out_data[i][0].strip()
			out_data[i][1] = out_data[i][1].strip()
			### Checking if there is success or unsuccess saved ###
			if "Date of last successfull scan" in out_data[i]:
				success=True
			if "Date of last unsuccessfull scan" in out_data[i]:
				fail=True
		### Writing data if it was successfull opeation ###
		if ok==True:
			### If success was previously written ###
			if success==True:
				if out_data[0][0]=="Date of last successfull scan":
					out_data[0][1]=str(datetime.date.today())
					out_data[1][1]=str(datetime.datetime.now().time())
					out_data[2][1]=person
				else:
					out_data[3][1]=str(datetime.date.today())
					out_data[4][1]=str(datetime.datetime.now().time())
					out_data[5][1]=person
			### if success was not previously written ###
			else:
				out_data.append(["Date of last successfull scan",str(datetime.date.today())])
				out_data.append(["Hour of last successfull scan", str(datetime.datetime.now().time())])
				out_data.append(["Person responsible",person])
		else:
			### if fail was previously written to file ###
			if fail==True:
				if out_data[0][0]=="Date of last unsuccessfull scan":
					out_data[0][1]=str(datetime.date.today())
					out_data[1][1]=str(datetime.datetime.now().time())
					out_data[2][1]=person
				else:
					out_data[3][1]=str(datetime.date.today())
					out_data[4][1]=str(datetime.datetime.now().time())
					out_data[5][1]=person
			### if fail was not previously written to file ###
			else:
				out_data.append(["Date of last unsuccessfull scan",str(datetime.date.today())])
				out_data.append(["Hour of last unsuccessfull scan", str(datetime.datetime.now().time())])
				out_data.append(["Person responsible",person])
		for i in range(len(out_data)):
			out_data[i]=out_data[i][0]+": "+out_data[i][1]+"\n"
		out=open("scan_params.txt","w")
		out.write(''.join(out_data))
		out.close()

### Function for drawing graph ###
def graph(neighbour):
	### Dictionary for keeping data to create graph ###
	neighborship_dict = {}

	### Calculatiing and adding nodes and edges to network ###
	for router in neighbour:
		for ip in router[1]:
			times = 0
			for router_second in neighbour:
				if router_second == router:
					continue
				for ip_net in router_second[2]:
					if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_net, strict=False):
						times = times + 1
			for router_second in neighbour:
				if router_second == router:
					continue
				for ip_net in router_second[2]:
					if times == 0:
						break
					if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_net, strict=False) and times == 1:
						neighborship_dict[(router_second[0], router[0])] = ip
						break
					if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_net, strict=False) and times > 1:
						neighborship_dict[str(ipaddress.ip_network(ip_net, strict=False)), router[0]] = ip

	### Creating graph ###
	G = nx.Graph()

	### Drawing graph and saving it to file ###
	G.add_edges_from(neighborship_dict.keys())
	pos = nx.spring_layout(G, k=0.1, iterations=70)
	nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif", font_weight="bold")
	nx.draw_networkx_edges(G, pos, width=4, alpha=0.4, edge_color='black')
	nx.draw_networkx_edge_labels(G, pos, neighborship_dict, label_pos=0.3, font_size=6)
	nx.draw(G, pos, node_size=800, with_labels=False, node_color='b')
	plt.savefig('static/topology.png')

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

	scan,done_ok = scan_params()

	if done_ok==True:
		empty=False
		data=formatting()
	else:
		empty=True
		data=[]

	path = os.path.dirname(os.path.realpath(__file__))+"\ip_range.txt\n"
	path_pass = os.path.dirname(os.path.realpath(__file__)) + "\passwords.txt\n"
	form=Start()

	if form.validate_on_submit():
		time.sleep(5)
		ip_list=ip_range()
		if len(ip_list)==0:
			scan_parametres(False,scan,form.name.data)
			return redirect(url_for("main"))
		password_list=passwords()
		ip_available = pingy(ip_list)
		if len(ip_available)==0:
			scan_parametres(False, scan, form.name.data)
			flash("No ability to ping any device with given IP adress. Check IP addresses in file and try again. ")
		else:
			scan_parametres(True, scan, form.name.data)
			flash("Ability to connect with devices in the network. Trying to establish ssh session in order to gather information. ")
		return redirect(url_for("main"))

	if scan==[]:
		scan_data=False
	else:
		scan_data=True
	return render_template("index.html",empty=empty, form=form, path=path, path_pass=path_pass,scan_params=scan, scan_data=scan_data,id="R1", data=data)

### shutdown route - closing web server ###
@app.route("/shutdown")
def shutdown():
	shutdown_server()
	return render_template("shutting.html")

### topology route - displays topology picture ###
@app.route("/topology")
def topology():
	no_file=True
	if os.path.exists("topology.png")==True:
		no_file=False
	return render_template("topology.html",no_file=no_file)

### help route - information about program and short description ###
@app.route("/help")
def help():
	return render_template("help.html")

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
https://stackoverflow.com/questions/6256043/css-position-loading-indicator-in-the-center-of-the-screen 
https://stackoverflow.com/questions/17859993/basic-css-how-to-overlay-a-div-with-semi-transparent-div-on-top
'''
