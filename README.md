# qlikconnect

qlikconnect
-------------
qlikconnect is the python library used to interact with Qliksense.It uses API to connect with Qliksense through webocket. This module can be use to do things like fetch qlik charts data, evaluate your expression through this and many more.

Installation
-------------

Installation is pretty straightforward using **pip** :
```
pip install qlikconnect
```
----------
Example
-------------
After installing the library, import **SenseConnect** class as below:
For **Localhost Qliksense Desktop :**
```
from qlikconnect import SenseConnect
sc = SenseConnect()
```
For **Enterprise **, certificate details will be required:
```
from qlikconnect import SenseConnect
sc = SenseConnect(domain ='site_domain_name',
				  port='site_port_number',
				  userdirectory='userdirectory',
				  userid='userid') 
```
Certificates also required named 'root.pem', 'client.pem' and 'client_key.pem' in the same folder as your app in which can be exported from qmc.
Also you can get the port, userdirectory and userid from qmc.

----------
Use Case
-------------
> - **To get the list of all apps :**
> sc.get_list_of_apps()
> - **To get last refreshed timestamp of an app :**
> sc.get_last_updated_status(appname)
> - **To evaluate an expression from an app :**
> sc.evaluate_expression(appname, expression,e_o_d=0)

----------
Requirement
-------------
```
> websocket_client
> python 3 (3.6 recommended)
```
