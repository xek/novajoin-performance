#!/usr/bin/python3

import json
from os import system
from platform import node
from urllib.request import Request, urlopen

params = {"metadata": {"ipa_enroll": "True"},
          "hostname": node().split('.', 1)[0]}

request = Request('{{ novajoin_url }}', json.dumps(params).encode())
result = json.loads(urlopen(request).read().decode())

system('ipa-client-install -U -w {ipaotp} '
       '--hostname {hostname} --realm {krb_realm}'.format(result))
