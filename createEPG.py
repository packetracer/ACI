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

tenant = raw_input("Tenant Name: ")
ap = raw_input("Application Profile: ")
vlans = []
f = open("vlans2.list","r")
#for vlan in f.read().splitlines():
#       vlans.append()
for vlan in f.read().splitlines():
        vlans.append(vlan)
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


cookie = getCookie()
