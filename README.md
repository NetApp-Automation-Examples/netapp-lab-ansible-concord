This lab is tweaked for Getting Started With ONTAP Automation Using Ansible lab.

To get up and running quickly, ssh into the awx vm once your lab is up and run this:

```curl https://raw.githubusercontent.com/johnwarlick/netapp-lab-ansible-concord/main/_bootstrap/bootstrap.sh -o bootstrap.sh && bash bootstrap.sh```

Then activate the venv. 

```cd /root/netapp-lab-ansible-concord && source venv/bin/activate```

I typically install VS code with the Remote Explorer extension so I can connect directly to it and have a nice file editor experience. 

# TODO 
- Wipe AWX and bootstrap concord
