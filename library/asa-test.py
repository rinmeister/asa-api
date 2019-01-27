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

def main():

    fields = {
        "host": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str" },
        "password": {"required": False, "type": "str"},
        "validate_certs": {"default": False, "type": "bool" },
	}

    module = AnsibleModule(argument_spec=fields)
    m_args = module.params
    ts = 'https://{}/api/tokenservices'.format(m_args['host'])
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
            module.exit_json(changed=False, meta=module.params)

if __name__ == '__main__':
    main()

