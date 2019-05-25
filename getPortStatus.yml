import requests
import sys
import login
import json
from jinja2 import Template
import getpass
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
#CONSTANTS
MAX_ATTEMPT = 3
#LOGIN AND RETURN AUTH COOKIE
cookie=""
def getCookies():
        user = raw_input("Username: ")
        pwd = getpass.getpass()
        cookies = login.login(user,pwd)
        if "ERROR" not in cookies:
                return cookies
        else:
                print "Login denied by APIC, try again"

def getPortStatus(node,port,cookie):
        cookies = {'APIC-cookie':cookie}
        urlt = """https://apic.lgh.org/api/node/mo/topology/pod-1/node-{{NODE}}/sys/phys-[eth1/{{PORT}}].json?&rsp-subtree-include=relations"""
        ut = Template(urlt)
        url = ut.render(NODE=node,PORT=port)
        result = requests.get(url,cookies=cookies,verify=False)
        if result.status_code==200:
                result=result.json()
                display(node,port,result)

def display(node,port,result):
        print "----------------------------------"
        print "Leaf "+node+" E1/"+port+" details"
        print "----------------------------------"
        print "Admin State: " +(result['imdata'][9]['l1PhysIf']['attributes']['adminSt'])
        print "Auto Negotiation: " +(result['imdata'][9]['l1PhysIf']['attributes']['autoNeg'])
        print "Switching State: " +(result['imdata'][9]['l1PhysIf']['attributes']['switchingSt'])
        print "Speed: " +(result['imdata'][9]['l1PhysIf']['attributes']['speed'])
        print "Encap VLAN ID: " + (result['imdata'][8]['nwPathEp']['attributes']['nativeEncap']).split('-')[1]
        print "----------------------------------"

def attemptLogin():
        cookie = getCookies()
        i = 1
        while True:
                if i == MAX_ATTEMPT:
                        print "Too many attempts.  Goodbye."
                        sys.exit()
                elif cookie == None:
                        i+=1
                        cookie = getCookies()
                else:
                        return cookie
                        break

def getNode():
        try:
                node = int(raw_input("Node: "))
                if node > 100 and node < 106:
                        return str(node)
                else:
                        print "Incorrect Leaf number, retry"
                        return getNode()
        except ValueError as e:
                print e
                return getPort()
def getPort():
        try:
                port = int(raw_input("Port "))
                if port > 0 and port < 49:
                        return str(port)
                else:
                        print "Incorrecct port number, retry"
                        return getPort()
        except ValueError as e:
                print e
                return getPort()

cookie=attemptLogin()
node = getNode()
port = getPort()
getPortStatus(node,port,cookie)
