#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: rigeld.health.query
short_description: Run a health query on a remote cluster via an Inventory Host
description:
  - Run a health query on a remote cluster via an Inventory Host
author:
- Adam Miller (@maxamillion)
requirements:
  - requests
options:
    port:
        description:
            - Port to connect to the health query endpoint on
        type: int
        default: 443
        required: false
    hostname:
        description:
          - Hostname of the health service
        type: str
        default: ""
        required: true
    data:
        description:
            - YAML dict of data payload to be serialized as JSON
              and used as data for the HTTP(S) transaction
        type: complex
        default: C({})
        required: false
    headers:
        description:
            - YAML dict of headers to be serialized as JSON and used as data
              for the HTTP(S) transaction
        type: complex
        default: C({'Content-Type': 'application/json'})
        required: true

'''

EXAMPLES = '''
# Note: set health_hostnames either as a playbook var or in inventory
- name: Run a query on a set of remote hosts
  rigeld.health.query:
    hostname: {{ item }}
    headers:
      statuskey: 'sekrit'
      Content-Type': 'application/json'
  loop: health_hostnames
'''

import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
import requests

def main():
    module = AnsibleModule(
        argument_spec=dict(
            port=dict(type='int', default=443),
            hostname=dict(type='str', default="", required=True),
            data=dict(type='dict', default={"name": "Top Table Counts"}),
            headers=dict(type='dict', default={}),
        ),
    )

    try:
        payload = module.params['data']
        headers = module.params['headers']
        url = f'{hostname}:{port}/api/v1/management/health?category=Database&name="Top Table Counts"'
        response = requests.request("POST", url, headers=headers, data=payload, timeout=600)

    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())

    module.exit_json(msg=response.content)


if __name__ == '__main__':
    main()
