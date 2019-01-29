#!/usr/bin/python3

import json
from os import system
from platform import node
from time import sleep
from urllib.request import Request, urlopen


### Set DNS

open('/etc/resolv.conf', 'w+').write('''
search example.test
nameserver {{ ipa_dns }}
''')

### Authenticate in Keystone

credentials = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "name": "nova",
                    "domain": {
                        "name": "Default"
                    },
                    "password": "{{ nova_password }}"
                }
            }
        },
        "scope": {
            "project": {
                "name": "service",
                "domain": {
                    "id": "default"
                }
            }
        }
    }
}

headers = {'Content-Type': 'application/json'}
request = Request('{{ keystone_url }}/v3/auth/tokens',
                  json.dumps(credentials).encode(), headers)
headers['X-Auth-Token'] = urlopen(request).info().get('X-Subject-Token')

### Create metadata with services, get hostname

example_services = ['mysql', 'rabbitmq', 'redis', 'neutron', 'novnc-proxy',
                    'HTTP', 'libvirt-vnc', 'haproxy']

hostname = node().split('.', 1)[0]
metadata = {"ipa_enroll": "True"}
for service in example_services:
    metadata['compact_service_' + service] = json.dumps(['test'])

params = {"metadata": metadata, "hostname": hostname}

### Get ipaotp from novajoin

request = Request('{{ novajoin_url }}/v1/', json.dumps(params).encode(), headers)
result = json.loads(urlopen(request).read().decode())

result['domain'] = result['krb_realm'].lower()

### Run IPA Client installation

system('ipa-client-install -U -N -w {ipaotp} --domain {domain} '
       '--hostname {hostname} --realm {krb_realm}'.format(**result))

### Request certificates

for service in example_services:
    system('ipa-getcert request -r '
           '-f /etc/pki/tls/certs/{hostname}-{service}.crt '
           '-k /etc/pki/tls/private/{hostname}-{service}.key '
           '-N CN={hostname}.test.{domain} -D {hostname}.{domain} '
           '-U id-kp-serverAuth '
           '-K {service}/{hostname}.test.{domain}'.format(
               hostname=hostname,
               domain=result['domain'],
               service=service))

sleep(60)
system('ipa-getcert list')
