#CREATE BRIDGE DOMAINS BASED ON LIST OF VLANS
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
#TAKE INPUT OF TENANT AND VRF FROM USER
tenant = raw_input("Tenant Name: ")
vrf = raw_input("VRF Name: ")
#READ LIST OF VLANS FROM VLANS.LIST
vlans = []
for vlan in f.read().splitlines():
        vlans.append(vlan)
        
#CREATE BRIDGE DOMAINS BASED ON LIST OF VLANS
def createBD(vlan,tenant,vrf,cookie):
        urltemplate = "https://{{hostname}}/api/node/mo/uni/tn-{{tenant}}/BD-{{VLAN}}-BD.json"
        ut = Template(urltemplate)
        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookie}

        payloadtemplate = """payload{
                "fvBD": {
                        "attributes": {
                                "dn": "uni/tn-{{tenant}}/BD-{{VLAN}}-BD",
                                "mac": "00:22:BD:F8:19:FF",
                                "name": "{{VLAN}}-BD",
                                "arpFlood": "true",
                                "unkMacUcastAct": "flood",
                                "unicastRoute": "false",
                                "rn": "BD-{{VLAN}}-BD",
                                "status": "created"
                        },
                        "children": [{
                                "fvRsCtx": {
                                        "attributes": {
                                                "tnFvCtxName": "{{VRF}}",
                                                "status": "created,modified"
                                        },
                                        "children": []
                                }
                        }]
                }
        }"""
        pt = Template(payloadtemplate)
        data = pt.render(tenant=tenant,VLAN=vlan,VRF=vrf)
        url = ut.render(tenant=tenant,VLAN=vlan,hostname=hostname)
        out = []
        result = (requests.post(url, data=data, headers=headers, cookies=cookies, verify=False))
        out.append(result.status_code)
        out.append(vlan+"-BD")
        out.append(result.text)
        return out

###########
cookie = getCookie()
suc=0
fail=0
#FOR EACH VLAN, CREATE A BRIDGE DOMAIN
for vlan in vlans:
        result = createBD(vlan,tenant,vrf,cookie)
        if result[0]==200:
                print result[1]+" created successfully"
                suc+=1
        else:
                print "Failure creating "+result[1]
                print result[2]
                fail+=1
#PRINT NUMBER OF SUCCESSFUL CREATES AND NUMBER OF FAILS                
print "Success: "+str(suc)
print "Fail: " +str(fail)
