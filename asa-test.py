def main()

    fields = {
        "host": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str" },
        "password": {"required": False, "type": "str"},
        "validate_certs": {"default": False, "type": "bool" },
	}

	module = AnsibleModule(argument_spec=fields)
	module.exit_json(changed=False, meta=module.params)

