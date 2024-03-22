#!/usr/bin/env python3
'''
This script takes a base64-encoded json payload as a CLI arg. This payload includes 
LIF information with IP addresses and pings each to verify they are up.
'''
import json
import base64
import sys
import os
import subprocess

# Get the payload from the CLI
lif_payload = base64.b64decode(sys.argv[1]).decode('utf-8')
ping_count = sys.argv[2] if sys.argv[2] else 5

# Load the payload into a dictionary
lifs = json.loads(lif_payload)

# Loop through each LIF and ping it
for lif in lifs:
    ip = lif['ip']['address']
    ping = subprocess.run(['ping', '-c', ping_count, ip], stdout=subprocess.PIPE)
    if ping.returncode == 0:
        print(f'{ip} is up')
    else:
        print(f'{ip} is down')



