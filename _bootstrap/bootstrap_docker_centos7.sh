#!/bin/sh
cd /root
git clone https://github.com/johnwarlick/netapp-lab-ansible-concord.git
cd netapp-lab-ansible-concord
yes | \cp -rf _bootstrap/CentOS-7-Base.repo /etc/yum.repos.d/CentOS-Base.repo
sudo yum install python3 -y
pip3 install --upgrade pip 
python3 -m venv venv
source venv/bin/activate
pip install ansible
ansible-galaxy role install geerlingguy.docker
ansible-playbook bootstrap_docker.yml