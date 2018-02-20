# cisco_project
Project to Cisco Incubator 5.0

Authors: Anna Luszczkiewicz, Kinga Slowik, Volodymyr Ushnevych

--- Description ---
This program is used for basic network analysis - such as how many routers are in network, what modules does they have, how the topology looks like. In our project we were trying to provide a tool that is easily expandable and friendly to the end user. According to such requirements we decided to create web server with all necessary elements - such solution provides universality to our solution and makes the usage of program more intuitive than traditional console. Considering also future development of our project we hope that thanks to used web server it will be easier for us to add more functions.

--- Requirements ---
Our project demands following intalled modules:
Python 3.6
flask
flask-bootstrap
flask-wtf
ipaddress
datetime
time
subprocess
re
matplotlib
networkx

To use our application necessary is also Web browser.

--- Running application ---
After download of all files in github, please make sure they are places in proper folders. Folder hierarchy:

project_all
-static:          //pictures
  --loading.gif
  --topology.png
 -templates       //all html files
  --base.html
  --index.html
  --shutting.html
  --topology.html
  --upload.html
 -config.py
 -final.txt
 -forms.py
 -graph.py
 -ip_range.txt
 -passwords.txt
 -project.py
 -scan_params.py
 
 In order to run our program type: python project.py
 The address of web server is: 127.0.0.1:5000
 
 When typing this address you will se main page of our program. In case of any troubles go to page: 127.0.0.1:5000/help (also you can click 'Documentation'), where there is instruction and short description of our program.
 
 We hope you will enjoy our project! 
