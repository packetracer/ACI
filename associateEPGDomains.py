#ASSOCIATES PHYSICAL AND L2-OUT DOMAINS TO EPG
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
hostname = '<IP OR FQDN OF APIC>'

#LOGIN AND GET COOKIE
def getCookie():
        user = raw_input("Username: ")
        pwd = getpass.getpass()
        cookie = login.login(user,pwd)
        if "ERROR" not in cookie:
                return cookie
        else:
                print cookie
                getCookie()
                
#GRAB TENANT AND APPLICATION PROFILE AS USER INPUIT
tenant = raw_input("Tenant Name: ")
ap = raw_input("Application Profile: ")

#GET LIST OF VLANS FROM VLANS.LIST
vlans = []
f = open("vlans.list","r")
for vlan in f.read().splitlines():
        vlans.append(vlan)

#ASSOCIATE PHYS-DOMAIN TO EPG
def assocPHYS(vlan,ap,tenant,cookie):
        urltemplate = "https://{{hostname}}/api/node/mo/uni/tn-{{TENANT}}/ap-{{AP}}/epg-{{VLAN}}-EPG.json"
        ut = Template(urltemplate)
        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookie}

        payloadtemplate = """payload{
        "fvRsDomAtt": {
                "attributes": {
                        "resImedcy": "immediate",
                        "tDn": "uni/phys-PHYS-DOMAIN",
                        "status": "created"
                },
                "children": []
        }
        }"""
        pt = Template(payloadtemplate)
        url = ut.render(TENANT=tenant,VLAN=vlan,hostname=hostname,AP=ap)
        data = pt.render()
        out = []
        result = (requests.post(url, data=data, headers=headers, cookies=cookies, verify=False))
        out.append(result.status_code)
        out.append("PHYS-DOMAIN")
        out.append(result.text)
        return out

#ASSOCIATE L2-OUT-DOMAIN TO EPG
def assocL2OUT(vlan,ap,tenant,cookie):
        urltemplate = "https://{{hostname}}/api/node/mo/uni/tn-{{TENANT}}/ap-{{AP}}/epg-{{VLAN}}-EPG.json"
        ut = Template(urltemplate)
        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookie}

        payloadtemplate = """payload{
        "fvRsDomAtt": {
                        "attributes": {
                        "resImedcy": "immediate",
                        "tDn": "uni/l2dom-L2-OUT-DOMAIN",
                        "status": "created"
                },
                "children": []
        }
        }"""
        pt = Template(payloadtemplate)
        url = ut.render(TENANT=tenant,VLAN=vlan,hostname=hostname,AP=ap)
        data = pt.render()
        out = []
        result = (requests.post(url, data=data, headers=headers, cookies=cookies, verify=False))
        out.append(result.status_code)
        out.append("L2-OUT-DOMAIN")
        out.append(result.text)
        return out

##################
cookie = getCookie()
psuccess = 0
pfail = 0
lsuccess = 0
lfail = 0
#FOR EACH VLAN IN VLAN LIST, ASSOCIATE PHYSICAL DOMAIN
for vlan in vlans:
        result = assocPHYS(vlan,ap,tenant,cookie)
        if result[0]==200:
                print result[1]+" successfully associated to "+vlan+"-EPG"
                psuccess+=1
        else:
                print "Failure associating "+result[1]
                print result[2]
                pfail+=1
#FOR EACH VLAN IN VLAN LIST,  ASSOCIATE L2 OUT DOMAIN
for vlan in vlans:
        result = assocL2OUT(vlan,ap,tenant,cookie)
        if result[0]==200:
                print result[1]+" successfully associated to "+vlan+"-EPG"
                lsuccess+=1
        else:
                print "Failure associating "+result[1]
                print result[2]
                lfail+=1
#PRINT SUCCESSES AND FAILS FOR EACH ASSOCIATION
print "Physical Domain Associations Successful: "+str(psuccess)
print "Physical Domain Associations Failed: "+str(pfail)
print "L2 Out Domain Associations Successful: "+str(lsuccess)
print "L2 Out Domain Associations Failed:"+str(lfail)
                                                              
