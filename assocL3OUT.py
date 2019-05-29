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

tenant = raw_input("Tenant Name: ")
l3out = raw_input("L3 Out Name: ")
vlans = []
f = open("vlans.list","r")
#for vlan in f.read().splitlines():
#       vlans.append()
for vlan in f.read().splitlines():
        vlans.append(vlan)

def assocL3OUT(tenant,l3out,cookie):
        urltemplate = "https://{{HOST}}/api/node/mo/uni/tn-{{TENANT}}/BD-{{VLAN}}-BD.json"
        ut = Template(urltemplate)
        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookie}
        payloadtemplate = """payload{
        "fvRsBDToOut": {
                "attributes": {
                        "tnL3extOutName": "{{L3OUT}}",
                        "status": "created"
                },
                "children": []
        }
}"""
        pt = Template(payloadtemplate)
        data = pt.render(L3OUT=l3out)
        url = ut.render(TENANT=tenant,VLAN=vlan,HOST=hostname)
        out = []
        result = (requests.post(url, data=data, headers=headers, cookies=cookies, verify=False))
        out.append(result.status_code)
        out.append(vlan+"-BD")
        out.append(result.text)
        return out

cookie = getCookie()
success = 0
fail = 0
print "***********BRIDGE ASSOCIATIONS*************"
for vlan in vlans:
        result = assocL3OUT(tenant,l3out,cookie)
        if result[0]==200:
                print result[1]+" associated successfully"
                success+=1
        else:
                print "Failure associating "+result[1]
                print result[2]
                fail+=1

print "BD Successful: "+str(success)
print "BD Failed: "+str(fail)
print "*********************************************"
