#!/bin/sh
sudo apt update 
sudo apt install python3-pip -y
sudo pip3 install ansible -y
pip3 install -r requirements.txt
ansible-galaxy collection install -r collections/requirements.yml
read -s -p "Password for ONTAP Clusters: " ONTAP_PASS
read -s -p "Password for AWX: " TOWER_PASS
read -s -p "Password for AIQUM: " AIQUM_PASS
export AIQUM_PASSWORD=$AIQUM_PASS
export ONTAP_PASSWORD=$ONTAP_PASS
export TOWER_PASSWORD=$TOWER_PASS
ansible-playbook _bootstrapawx.yml