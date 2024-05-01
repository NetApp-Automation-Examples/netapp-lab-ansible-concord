#!/bin/sh
cd /root
git clone https://github.com/johnwarlick/netapp-lab-ansible-concord.git
cd netapp-lab-ansible-concord
dnf install python3.9 -y
python3 -m venv venv
source venv/bin/activate
cd ansible
pip install --upgrade pip setuptools
pip install -r requirements.txt
ansible-galaxy role install -r roles/requirements.yml
