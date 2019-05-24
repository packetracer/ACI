
hostname = '<APIC IP OR FQDN>'

#LOGIN AND GET COOKIE
def getCookie():
        user = raw_input("Username: ")
        pwd = getpass.getpass()
        cookie = login.login(user,pwd)
        if "ERROR" not in cookie:
                return cookie
#VARIABLES
#THIS CREATES BD for ONE TENANT/VRF COMBINATION PER EXECUTION BASED ON VLAN NAMES LISTED IN vlans.list
tenant = raw_input("Tenant Name: ")
vrf = raw_input("VRF Name: ")
vlans = []
f = open("vlans.list","r")
for vlan in f.read().splitlines():
        vlans.append(vlan)

#CREATE FLOODING BD (CHANGE VALUES TO MEET YOUR NEEDS)
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


cookie = getCookie()
for vlan in vlans:
        result = createBD(vlan,tenant,vrf,cookie)
        if result[0]==200:
                print result[1]+" created successfully"
        else:
                print "Failure creating "+result[1]
                print result[2]
