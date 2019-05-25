import requests
import sys
import login
import json
from jinja2 import Template
import getpass
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
#CONSTANTS
MAX_ATTEMPT = 3
#LOGIN AND RETURN AUTH COOKIE
def getCookies():
        user = raw_input("Username: ")
        pwd = getpass.getpass()
        cookies = login.login(user,pwd)
        if "ERROR" not in cookies:
                return cookies
        else:
                print "Login denied by APIC, try again"

tenant = raw_input("Tenant: ")
ap = raw_input("App Profile: ")

#LIST EPGS
def listEPGs(tenant,ap,cookie):
        cookies = {'APIC-cookie':cookie}
        urlt = """https://apic.lgh.org/api/node/mo/uni/tn-{{TENANT}}/ap-{{AP}}.json?query-target=subtree&target-subtree-class=fvAEPg&query-target-filter=and(not(wcard(polUni.dn, "__ui_")),eq(fvAEPg.isAttrBasedEPg,"false"))&query-target=subtree&target-subtree-class=fvRsProv,fvRsCons,tagAliasInst"""
        ut = Template(urlt)
        url = ut.render(TENANT=tenant,AP=ap)
        result = requests.get(url,cookies=cookies,verify=False)
        result=result.json()
        last = int(result['totalCount'])
        print "TOTAL ENTRIES: " + str(last)
        for i in range(0,last):
                print "EPG#{}: ".format(str(i+1))+ (result['imdata'][i]['fvAEPg']['attributes']['name'])

def attemptLogin():
        cookie = getCookies()
        i = 1
        while True:
                if i == MAX_ATTEMPT:
                        print "Too many attempts.  Goodbye."
                        sys.exit()
                                        elif cookie == None:
                        i+=1
                        cookie = getCookies()
                else:
                        return cookie
                        break

cookie = attemptLogin()
listEPGs(tenant,ap,cookie)
