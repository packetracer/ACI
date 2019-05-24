import requests
import sys
import getpass
import xmltodict, json
#use pip install xmltodict if you get a module error

#ACCEPT USER INPUT FOR LOGIN
#user = raw_input("User: ")
#pwd = getpass.getpass(

#HARDCODED LOGIN INFORMATION:
user = '<ADMIN USER>'
pwd = '<PASSWORD>'

#VARIABLES
host = '<APIC IP OR FQDN>'
url  = 'https://{}/api/aaaLogin.xml'.format(host)
xml =  """<aaaUser name='{0}' pwd ='{1}'/>""".format(user,pwd)
headers = {'Content-Type': 'application/xml'} 

#LOGIN FUNCTION, RETURNS AUTH COOKIE IF SUCCESSFUL
def login():
        try:
                result = ((xmltodict.parse(requests.post(url, data=xml, headers=headers, verify=False).text)))
                if "DENIED" in str(result):
                        return "Login denied by APIC"
                else:
                        return result['imdata']['aaaLogin']['@token']
        except requests.exceptions.Timeout:
                return "Request timed out."
        except requests.exceptions.TooManyRedirects:
                return "Too many redirects."
        except requests.exceptions.RequestException as e:
                return "Error " + str(e)
#IF LOGIN SUCCESSFUL, RETURN APIC COOKIE
def main():
        print login()
        #THIS IS THE VALUE of "APIC-cookie"
        #DO WHAT YOU WANT WITH THIS OUTPUT.  In my system I will write the cookie to a file "cookie" which will be read
        #by other scripts

if __name__== "__main__":
        main()
