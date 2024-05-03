Using the Nondisruptive Operations for NetApp ONTAP 9.10.1 v3.0 lab, ssh into the rhel1 vm once your lab is up and run the following. I typically install VS code with the Remote Explorer extension so I can connect directly to it and have a nice file editor experience. 

```curl https://raw.githubusercontent.com/johnwarlick/netapp-lab-ansible-concord/main/_bootstrap/bootstrap.sh -o bootstrap.sh && bash bootstrap.sh```

Then activate the venv and set ONTAP_PASSWORD. 

```cd /root/netapp-lab-ansible-concord && source venv/bin/activate```
```export ONTAP_PASSWORD=<thepsswd>```

To stand up concord, cd into ansible and run the boostrap_concord.yml playbook. There's a weird issue with the github_deploy_key ansible module so you'll have to add that public key to github manually for now, but everything else is automated.

Shout out to https://github.com/rif/spark, a nice lil http server that works great for testing upgrades in a LOD. 