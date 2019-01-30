#!/usr/bin/python

DOCUMENTATION = '''
---

module: asa-test

'''

from ansible.module_utils.basic import *
import json
import requests
import os
import urllib3

#Specify in variable fields all variables in playbook YAML
fields = {
    "host": {"required": True, "type": "str"},
    "username": {"required": True, "type": "str" },
    "password": {"required": False, "type": "str"},
    "validate_certs": {"default": False, "type": "bool" },
    }

#module is the class containing the attributes defined in 'fields'
module = AnsibleModule(argument_spec=fields)
#m_args contains the dictionary of the variables
m_args = module.params
#path = '{}/.config'.format(os.path.expanduser('~'))
path = os.path.expanduser('~')
ts = 'https://{}/api/tokenservices'.format(m_args['host'])
test = 'https://{}/api/monitoring/clock'.format(m_args['host'])
mainurl= 'https://{}/api/cli'.format(m_args['host'])
token = ''

def login():
    while True:
        username = m_args['username']
        password = m_args['password']
        try:
            r = requests.post(ts, auth=(username, password), verify=False)
            token = r.headers['X-Auth-Token']
            tokenFile = open("%s/tokenfile" % path,"w")
            tokenFile.write(token)
            tokenFile.close()
            os.chmod('%s/tokenfile' %path, 0o600)
            break
        except KeyError:
             module.fail_json(msg='There is a keyerror')
#    module.exit_json(changed=False, meta=module.params, msg='done')

def aanmeldpoging():
    while True:
        if os.path.isfile('%s/tokenfile' % path):
            try:
                with open('%s/tokenfile' %path, 'r') as jar:
                        r = requests.get(test, headers={'X-Auth-Token': '%s' % jar.readline()}, verify=False)
                        if r.status_code == 401:
                            login()
                        break
            except ValueError:
                module.failed_json(msg='someone tinkered with the token, it is invalid, you will have to login again.')
                login()
            jar.close()
        else:
            login()


def main():

# Probeer aan te melden met een token
    aanmeldpoging()
    with open('%s/tokenfile' %path, 'r') as jar:
        r = requests.post(mainurl, headers={'X-Auth-Token': '%s' % jar.readline()}, json={"commands": ["show running-config"]}, verify=False)
        jar.close()
    r_json = r.json()
    with open('{}/showrun'.format(path),'w') as showrun:
        json.dump(r_json, showrun)
    module.exit_json(changed=True, meta=module.params, msg='show running has been saved into your home directory')

if __name__ == '__main__':
    main()

