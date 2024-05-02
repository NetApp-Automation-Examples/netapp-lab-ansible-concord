#!/usr/bin/env python
'''
This script takes a base64-encoded json payload from an Ansible playbook as the first CLI arg. 
This payload includes LIF information with IP addresses and pings each to verify they are up. 

The second CLI arg is the number of pings to send to each LIF. If no value is provided, 
the default is 5 pings. 

The third CLI arg is the amount of times to run the ping tests. If no value is provided, the default is 2.

The fourth CLI arg is the amount of time to pause between each test run. If no value is provided, the
default is 10 seconds.

If 'mock' is passed as the fifth cli arg, the ping tests will not actually run, and failed_pings will be left at 0

Finally, the resulting JSON payload is printed out for the Ansible playbook with an 
incremented failed_pings counter

'''
import time
import json
import base64
import sys
import subprocess

# Get the payload from the CLI
lif_payload = base64.b64decode(sys.argv[1]).decode('utf-8')
ping_count = sys.argv[2] if sys.argv[2] else 5
test_count = sys.argv[3] if sys.argv[3] else 2
test_pause = sys.argv[4] if sys.argv[4] else 10
try: 
    if sys.argv[5] == 'mock':
        mock = True
except IndexError:
    mock = False

# Load the payload into a dictionary
lifs = json.loads(lif_payload)

# Loop through the amount of times to run the ping tests
for i in range(int(test_count)):
    # Loop through each LIF and ping it
    for lif in lifs:
        ip = lif['ip']['address']

        if lif.get('failed_pings') is None:
            lif['failed_pings'] = 0
        
        if mock: 
            continue; 
        
        ping = subprocess.run(['ping', '-c', ping_count, ip], stdout=subprocess.PIPE)
        
        if ping.returncode != 0:
            # increment failed_pings count if ping fails
            lif['failed_pings'] += 1

    time.sleep(int(test_pause))
               
# return json back to Ansible playbook
print(json.dumps(lifs, indent=2))