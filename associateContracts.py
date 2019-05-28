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
hostname = '<APIC IP OR FQDN HERE>'

#LOGIN AND GET COOKIE
def getCookie():
        user = raw_input("Username: ")
        pwd = getpass.getpass()
        cookie = login.login(user,pwd)
        if "ERROR" not in cookie:
                return cookie

#ACCEPT USER INPUT FOR TENANT, APPLICATION PROFILE, PROVIDER AND CONSUMER CONTRACT NAMES
tenant = raw_input("Tenant Name: ")
ap = raw_input("Application Profile: ")
pcontract = raw_input("Provider Contract: " )
ccontract = raw_input("Consumer Contract: ")

#READ IN LIST OF VLANS FOR EPGs
vlans = []
f = open("vlans.list","r")
for vlan in f.read().splitlines():
        vlans.append(vlan)
        
#ASSOCIATE PROVIDER CONTRACTS PER EPG        
def assocProvider(vlan,ap,tenant,contract,cookie):
        urltemplate = "https://{{HOST}}/api/node/mo/uni/tn-{{TENANT}}/ap-{{AP}}/epg-{{VLAN}}-EPG.json"
        ut = Template(urltemplate)
        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookie}

        payloadtemplate = """payload{
        "fvRsProv": {
                "attributes": {
                        "tnVzBrCPName": "{{CONTRACT}}",
                        "status": "created,modified"
                },
                "children": []
        }
}"""
        pt = Template(payloadtemplate)
        data = pt.render(CONTRACT=contract)
        url = ut.render(TENANT=tenant,VLAN=vlan,HOST=hostname,AP=ap)
        out = []
        result = (requests.post(url, data=data, headers=headers, cookies=cookies, verify=False))
        out.append(result.status_code)
        out.append(vlan+"-EPG")
        out.append(result.text)
        return out

#ASSOCIATE CONSUMER CONTRACTS PER EPG
def assocConsumer(vlan,ap,tenant,contract,cookie):
        urltemplate = "https://{{HOST}}/api/node/mo/uni/tn-{{TENANT}}/ap-{{AP}}/epg-{{VLAN}}-EPG.json"
        ut = Template(urltemplate)
        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookie}

        payloadtemplate = """payload{
        "fvRsCons": {
                "attributes": {
                        "tnVzBrCPName": "{{CONTRACT}}",
                        "status": "created,modified"
                },
                "children": []
        }
}"""
        pt = Template(payloadtemplate)
        data = pt.render(CONTRACT=contract)
        url = ut.render(TENANT=tenant,VLAN=vlan,HOST=hostname,AP=ap)
        out = []
        result = (requests.post(url, data=data, headers=headers, cookies=cookies, verify=False))
        out.append(result.status_code)
        out.append(vlan+"-EPG")
        out.append(result.text)
        return out

cookie = getCookie()
success = 0
fail = 0
#ASSOCIATE PROVIDER CONTRACTS
print "************PROVIDER ASSOCIATIONS************"
for vlan in vlans:
        result = assocProvider(vlan,ap,tenant,pcontract,cookie)
        if result[0]==200:
                print result[1]+" associated successfully"
                success+=1
        else:
                print "Failure associating "+result[1]
        else:
                print "Failure associating "+result[1]
                print result[2]
                fail+=1

print "Provider Successful: "+str(success)
print "Provider Failed: "+str(fail)

success = 0
fail = 0
print "*********************************************"
#ASSOCIATE CONSUMER CONTRACTS
print "***********CONSUMER ASSOCIATIONS*************"
for vlan in vlans:
        result = assocConsumer(vlan,ap,tenant,ccontract,cookie)
        if result[0]==200:
                print result[1]+" associated successfully"
                success+=1
        else:
                print "Failure associating "+result[1]
                print result[2]
                fail+=1

print "Consumer Successful: "+str(success)
print "Consumer Failed: "+str(fail)
print "*********************************************"
