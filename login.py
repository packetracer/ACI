import requests
import sys
import getpass
import xmltodict, json
#use pip install xmltodict if you get a module error

#VARIABLES
host = 'apic.lgh.org'
url  = 'https://{}/api/aaaLogin.xml'.format(host)
xml =  """<aaaUser name='{0}' pwd ='{1}'/>""".format(user,pwd)
headers = {'Content-Type': 'application/xml'} # set what your server accepts

#LOGIN FUNCTION, RETURNS AUTH COOKIE IF SUCCESSFUL
def login(user,pwd):
        host = 'apic.lgh.org'
        url  = 'https://{}/api/aaaLogin.xml'.format(host)
        xml =  """<aaaUser name='{0}' pwd ='{1}'/>""".format(user,pwd)
        headers = {'Content-Type': 'application/xml'} # set what your server accepts

        try:
                result = ((xmltodict.parse(requests.post(url, data=xml, headers=headers, verify=False).text)))
                if "DENIED" in str(result):
                        return "ERROR: Login denied by APIC"
                else:
                        return result['imdata']['aaaLogin']['@token']
        except requests.exceptions.Timeout:
                return "ERROR: Request timed out."
        except requests.exceptions.TooManyRedirects:
                return "ERROR: Too many redirects."
        except requests.exceptions.RequestException as e:
                return "ERROR: " + str(e)

def main():
        return login(user,pwd)

if __name__== "__main__":
        main()
