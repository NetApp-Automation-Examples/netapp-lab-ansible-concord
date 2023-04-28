#!/bin/sh
cd /root
git clone https://github.com/johnwarlick/netapp-lab-ansible-concord.git
# This Centos8 is busted so we gotta fix dnf first
yes | \cp -rf netapp-ontap-ansible-awx-demo/_bootstrap/CentOS-Base.repo /etc/yum.repos.d/
yes | \cp -rf netapp-ontap-ansible-awx-demo/_bootstrap/CentOS-AppStream.repo /etc/yum.repos.d/
#rpm --rebuilddb
# 3.9 gives an error TODO - fix error and update to 3.9
dnf install python3.8 -y
sudo alternatives --set python3 /usr/bin/python3.8
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
if [ x"${ONTAP_PASS}" == "x" ]; then 
    read -s -p "Password for ONTAP Clusters: " ONTAP_PASS
fi
export ONTAP_PASSWORD=$ONTAP_PASS
