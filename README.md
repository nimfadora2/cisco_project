# cisco_project
Project to Cisco Incubator 5.0

Authors: Anna Luszczkiewicz, Kinga Slowik, Volodymyr Ushnevych

--- Description ---

This program is used for basic network analysis - such as how many routers are in network, what modules does they have, how the topology looks like. In our project we were trying to provide a tool that is easily expandable and friendly to the end user. According to such requirements we decided to create web server with all necessary elements - such solution provides universality to our solution and makes the usage of program more intuitive than traditional console. Considering also future development of our project we hope that thanks to used web server it will be easier for us to add more functions.

--- Requirements ---

Our project demands following intalled modules:<br />
Python 3.6<br />
flask<br />
flask-bootstrap<br />
flask-wtf<br />
ipaddress<br />
datetime<br />
time<br />
subprocess<br />
re<br />
matplotlib<br />
networkx<br />
paramiko<br />


To use our application necessary is also Web browser.<br />

--- Running application ---<br />

After download of all files in github, please make sure they are places in proper folders. Folder hierarchy:

project_all
-static:          //pictures and website files <br />
  --bootstrap<br />
    ---- jquery-3.3.1.js<br />
    ---- css<br />
      ------ bootstrap.css<br />
    ---- js<br />
      ------ bootstrap.js<br />
  --loading.gif<br />
  --topology.png<br />
 -templates       //all html files<br />
  --base.html<br />
  --index.html<br />
  --shutting.html<br />
  --topology.html<br />
  --upload.html<br />
 -config.py<br />
 -final.txt<br />
 -forms.py<br />
 -ip_range.txt<br />
 -passwords.txt<br />
 -project.py<br />
 -scan_params.py<br />
 
 In order to run our program type: python3 project.py<br />
 The address of web server is: 127.0.0.1:5000<br />
 
 When typing this address you will se main page of our program. In case of any troubles go to page: 127.0.0.1:5000/help (also you can click 'Documentation'), where there is instruction and short description of our program.<br />
 
 We hope you will enjoy our project! 
