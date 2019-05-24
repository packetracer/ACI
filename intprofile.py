import requests
from jinja2 import Template
#use pip install jinja2 if you get a module error
import sys

def getCookie():
        f = open(cookie,'r')
        f.read()
        print f
node = "105"
port = "48"
hostname = 'apic.lgh.org'
urltemplate = "https://{{hostname}}/api/node/mo/uni/infra/accportprof-LEAF{{node}}.json"
ut = Template(urltemplate)
headers = {'Content-Type': 'application/json'}
cookies = {'APIC-cookie':sys.argv[1]}
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
print data
print url
print requests.post(url, data=data, headers=headers, cookies=cookies, verify=False).text
