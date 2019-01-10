#!/usr/bin/python3

import json
from os import system
from platform import node
from time import sleep
from urllib.request import Request, urlopen


example_services = ['mysql', 'rabbitmq', 'redis', 'neutron', 'novnc-proxy',
                    'HTTP', 'libvirt-vnc', 'haproxy']

hostname = node().split('.', 1)[0]
metadata = {"ipa_enroll": "True"}
for service in example_services:
    metadata['compact_service_' + service] = json.dumps(['test'])

params = {"metadata": metadata, "hostname": hostname}

request = Request('{{ novajoin_url }}', json.dumps(params).encode())
result = json.loads(urlopen(request).read().decode())

system('ipa-client-install -U -w {ipaotp} '
       '--hostname {hostname} --realm {krb_realm}'.format(result))

for service in example_services:
    system('ipa-getcert request -r '
           '-f /etc/pki/tls/certs/{hostname}-{service}.crt '
           '-k /etc/pki/tls/private/{hostname}-{service}.key '
           '-N CN={hostname}.test.{domain} -D {hostname}.{domain} '
           '-U id-kp-serverAuth '
           '-K {service}/{hostname}.test.{domain}`'.format({
               'hostname': hostname,
               'domain': result['krb_realm'].lower(),
               'service': service}))

sleep(60)
system('ipa-getcert list')
