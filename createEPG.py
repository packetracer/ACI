#CREATES EPGS BASED ON LIST OF VLANS
import requests
from jinja2 import Template
#use pip install jinja2 if you get a module error
import sys
import login
import getpass
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
#CONSTANTS
hostname = 'apic.lgh.org'

#LOGIN AND GET COOKIE
def getCookie():
        user = raw_input("Username: ")
        pwd = getpass.getpass()
        cookie = login.login(user,pwd)
        if "ERROR" not in cookie:
                return cookie

#GRAB TENANT AND APPLICATION PROFILE AS USER INPUT
tenant = raw_input("Tenant Name: ")
ap = raw_input("Application Profile: ")
#GET LIST OF VLANS IN VLANS.LIST
vlans = []
f = open("vlans.list","r")
for vlan in f.read().splitlines():
        vlans.append(vlan)

#CREATE EPG FOR VLAN
def createEPG(vlan,ap,tenant,cookie):
        urltemplate = "https://{{hostname}}/api/node/mo/uni/tn-{{tenant}}/ap-{{AP}}/epg-{{VLAN}}-EPG.json"
        ut = Template(urltemplate)
        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookie}

        payloadtemplate = """payload{
        "fvAEPg": {
                "attributes": {
                        "dn": "uni/tn-{{TENANT}}/ap-{{AP}}/epg-{{VLAN}}-EPG",
                        "name": "{{VLAN}}-EPG",
                        "rn": "epg-{{VLAN}}-EPG",
                        "status": "created"
                },
                "children": [{
                        "fvRsBd": {
                                "attributes": {
                                        "tnFvBDName": "{{VLAN}}-BD",
                                        "status": "created,modified"
                                },
                                "children": []
                        }
                }]
        }
}"""

        pt = Template(payloadtemplate)
        data = pt.render(TENANT=tenant,VLAN=vlan,AP=ap)
        url = ut.render(tenant=tenant,VLAN=vlan,hostname=hostname,AP=ap)
        out = []
        result = (requests.post(url, data=data, headers=headers, cookies=cookies, verify=False))
        out.append(result.status_code)
        out.append(vlan+"-EPG")
        out.append(result.text)
        return out

################3
cookie = getCookie()
#FOR EACH VLAN IN VLAN LIST, CREATE EPG
for vlan in vlans:
        result = createEPG(vlan,ap,tenant,cookie)
        if result[0]==200:
                print result[1]+" created successfully"
        else:
                print "Failure creating "+result[1]
                print result[2]
