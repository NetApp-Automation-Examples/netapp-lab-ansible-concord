Using the Nondisruptive Operations for NetApp ONTAP 9.10.1 v3.0 lab, ssh into the rhel1 vm once your lab is up and run this:

```curl https://raw.githubusercontent.com/johnwarlick/netapp-lab-ansible-concord/main/_bootstrap/bootstrap.sh -o bootstrap.sh && bash bootstrap.sh```

Then activate the venv. 

```cd /root/netapp-lab-ansible-concord && source venv/bin/activate```

I typically install VS code with the Remote Explorer extension so I can connect directly to it and have a nice file editor experience. 

# TODO 
- Bootstrap concord as well
