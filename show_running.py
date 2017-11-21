import json
import requests
import os
import getpass
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
ts = 'https://10.10.0.3/api/tokenservices'
test = 'https://10.10.0.3/api/monitoring/clock'
mainurl= 'https://10.10.0.3/api/cli'
path = '%s/.config' % os.path.expanduser('~')
token = ''
def login():
    while True:
        username = raw_input('Username: ')
        password = getpass.getpass(prompt='Password: ')
        try:
            r = requests.post(ts, auth=(username, password), verify=False)
            token = r.headers['X-Auth-Token']
            tokenFile = open("%s/tokenfile" % path,"w")
            tokenFile.write(token)
            tokenFile.close()
            os.chmod('%s/tokenfile' %path, 0o600)
            break
        except KeyError:
            print ("Wrong UID or password, please try again.")

def aanmeldpoging():
    while True:
        if os.path.isfile('%s/tokenfile' % path):
            try:
                with open('%s/tokenfile' %path, 'r') as jar:
                        r = requests.get(test, headers={'X-Auth-Token': '%s' % jar.readline()}, verify=False)
                        if r.status_code == 401:
                            login()
#                        print(r.url)
#                        print r.text
#                        print r.status_code
                        break
            except ValueError:
                print ("someone tinkered with the token, it is invalid, you will have to login again.")
                login()
            jar.close()
        else:
            login()

def main():
    with open('%s/tokenfile' %path, 'r') as jar:
        r = requests.post(mainurl, headers={'X-Auth-Token': '%s' % jar.readline()}, json={"commands": ["show running-config"]}, verify=False)
        jar.close()
    r_json = r.json()
#   r_json = r.text
    with open('showrun','w') as showrun:
        json.dump(r_json, showrun)
#       showrun.write(r_json)
#       showrun.close()
    #print r.text
    #print r.json()

aanmeldpoging()
main()
