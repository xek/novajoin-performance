# novajoin-performance
novajoin performance tests

## Running the test

To install dependencies, build images and run the test, execute:
```bash
ansible-playbook play.yaml
```

To rebuild images or only execute the test, execute individual playbooks in `playbooks/`.

The ansible scripts are tested to work on Fedora 28.

### Each client runs with the following scenario:

1. client calls novajoin HTTP api [done]
1. novajoin adds host to FreeIPA and gets an otp [done]
1. novajoin creates service entries in FreeIPA for that host [done]
1. client calls ipa-client-install with OTP, inside a container [done]
1. client gets keytab [done]
1. client requests a list of certs for the previously created service entries [buggy]
1. client gets the CRL [buggy]
