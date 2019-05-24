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
mynode = raw_input("Node number: ")
beginport = raw_input("From Port: ")
endport = raw_input("To Port: ")
hostname = 'apic.lgh.org'

#LOGIN AND GET COOKIE
def getCookie():
        user = raw_input("Username: ")
        pwd = getpass.getpass()
        cookie = login.login(user,pwd)
        if "ERROR" not in cookie:
                return cookie

def createPortProfile(cookie,node,port):
        urltemplate = "https://{{hostname}}/api/node/mo/uni/infra/accportprof-LEAF{{node}}.json"
        ut = Template(urltemplate)
        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookie}

        payloadtemplate = """payload{
                "infraHPortS": {
                        "attributes": {
                                "dn": "uni/infra/accportprof-LEAF{{node}}/hports-E{{port}}-typ-range",
                                "name": "E{{port}}",
                                "rn": "hports-E{{port}}-typ-range",
                                "status": "created,modified"
                        },
                        "children": [{
                                "infraPortBlk": {
                                        "attributes": {
                                                "dn": "uni/infra/accportprof-LEAF{{node}}/hports-E{{port}}-typ-range/portblk-block2",
                                                "fromPort": "{{port}}",
                                                "toPort": "{{port}}",
                                                "name": "block2",
                                                "rn": "portblk-block2",
                                                "status": "created,modified"
                                        },
                                        "children": []
                                }
                        },
                        {
                                "infraRsAccBaseGrp": {
                                        "attributes": {
                                                "tDn": "uni/infra/funcprof/accportgrp-DISABLED",
                                                "status": "created,modified"
                                        },
                                        "children": []
                                }
                        }]
                }
        }"""

        pt = Template(payloadtemplate)
        data = pt.render(node=node,port=port)
        url = ut.render(node=node,hostname=hostname)
        out = []
        out.append(requests.post(url, data=data, headers=headers, cookies=cookies, verify=False).status_code)
        out.append("Node: {0} Port: {1}".format(node,port))
        return out


cookie = getCookie()
for port in range(int(beginport),int(endport)+1):
        result = []
        result = createPortProfile(cookie,mynode,port)
        if result[0]==200:
                print result[1] + " created successfully"
        else:
                print "Failed to create " + result[1]

