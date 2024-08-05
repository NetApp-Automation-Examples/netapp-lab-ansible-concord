#!/bin/sh
cd /root
git clone https://github.com/johnwarlick/netapp-lab-ansible-concord.git
cd netapp-lab-ansible-concord
yes | \cp -rf _bootstrap/CentOS-7-Base.repo /etc/yum.repos.d/CentOS-Base.repo
sudo yum install python3 pip -y
sudo yum install gcc openssl-devel bzip2-devel libffi-devel -y
cd /usr/local/src
wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
tar -xvf Python-3.9.6.tgz
cd Python-3.9.6
autoconf
./configure --prefix=/usr/local/
sudo make
sudo make altinstall
sudo update-alternatives --install /usr/local/bin/python3 python3 /usr/local/bin/python3.9 1
sudo alternatives --set python3 /usr/local/bin/python3.9
cd /root/netapp-lab-ansible-concord
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
