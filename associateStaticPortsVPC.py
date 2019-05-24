#ASSIGN STATIC PORTS TO EPG OF TYPE VPC
#THIS IS WHERE THINGS GET REALLY ORG SPECIFIC.  THIS ONE REQUIRES A LIST OF VPCS TO ASSOCIATE TO STATIC PORTS.
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
#GRAB VLANS AND VPCS FROM RESPECTIVE LIST FILES
vlans = []
vpcs = []
f = open("vlans.list","r")
for vlan in f.read().splitlines():
        vlans.append(vlan)
f.close()
f = open("vpcs.list","r")
for vpc in f.read().splitlines():
        vpcs.append(vpc)
        
#CREATE VPC ASSOCIATIONS FOR EACH EPG
def associateStaticVPCs(vlan,ap,tenant,cookie):
        urltemplate = "https://{{hostname}}/api/node/mo/uni/tn-{{TENANT}}/ap-{{AP}}/epg-{{VLAN}}-EPG.json"
        ut = Template(urltemplate)
        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookie}
        for vpc in vpcs:
                vid = vlan.split('VLAN')[1]
                payloadtemplate = """payload{
                        fvRsPathAtt": {
                                "attributes": {
                                        "encap": "vlan-{{VID}}",
                                        "tDn": "topology/pod-1/protpaths-101-102/pathep-[{{VPC}}]",
                                        "status": "created"
                                },
                                "children": []
                        }
                }"""
                pt = Template(payloadtemplate)
                data = pt.render(VID=vid,VPC=vpc)
                url = ut.render(TENANT=tenant,VLAN=vlan,hostname=hostname,AP=ap)
                out = []
                result = (requests.post(url, data=data, headers=headers, cookies=cookies, verify=False))
                out.append(result.status_code)
                out.append(vlan+"-EPG")
                out.append(result.text)
        return out

################
cookie = getCookie()
for vlan in vlans:
        results = associateStaticVPCs(vlan,ap,tenant,cookie)
        for result in results:
                print result
