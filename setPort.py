import login,sys,requests,getpass
from jinja2 import Template
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

def getCookie():
        user = raw_input("Username: ")
        pwd = getpass.getpass()
        cookie = login.login(user,pwd)
        if "ERROR" not in cookie:
                return cookie

def disablePort(node,port,cookies,pg):
        urlt = 'https://apic.lgh.org/api/node/mo/uni/infra/accportprof-LEAF{{LEAF}}/hports-E{{PORT}}-typ-range/rsaccBaseGrp.json'
        ut = Template(urlt)

        headers = {'Content-Type': 'application/json'}
        cookies = {'APIC-cookie':cookies}
        url = ut.render(LEAF=node, PORT=port)
        datat = """payload{"infraRsAccBaseGrp":{"attributes":{"tDn":"uni/infra/funcprof/accportgrp-{{PG}}"},"children":[]}}"""
        dt = Template(datat)
        data = dt.render(PG=pg)
        return requests.post(url,data=data, headers=headers, cookies=cookies,verify=False)

def getPolicy():
        print "Please enter number of desired policy group: "
        print "1. DISABLED"
        print "2. 1G-ACCESS-PG"
        print "3. 100M-ACCESS-PG"
        print "4. AUTO-ACCESS-PG"
        try:
                pg = int(raw_input("#: "))
                if pg == 1:
                        return "DISABLED"
                if pg == 2:
                        return "1G-ACCESS-PG"
                if pg == 3:
                        return "100M-ACCESS-PG"
                if pg ==4:
                        return "AUTO-ACCESS-PG"
        except ValueError as e:
                print "Incorrect input value, try again."
                getPolicy()

if len(sys.argv) < 3:
        print "Missing required arguments, requires 2 but {} given.".format(str(len(sys.argv)-1))
else:
        node = int(sys.argv[1])
        if node > 100 and node < 103:
                print "Sorry, you cannot set 93180YC-EX ports with this script"
        elif node > 102 and node < 106:
                pg = getPolicy()
                cookie = getCookie()
                result = disablePort(sys.argv[1],sys.argv[2],cookie,pg)
                if result.status_code == 200:
                        print "LEAF{0}/E{1}".format(sys.argv[1],sys.argv[2])+" set as: "+ pg
                else:
                        print result.text

        else:
                print "Invalid Leaf Node "+str(node)+".  Try again."
