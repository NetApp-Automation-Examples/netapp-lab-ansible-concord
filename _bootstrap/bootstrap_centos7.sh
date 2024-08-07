#!/bin/sh
cd /root
git clone https://github.com/johnwarlick/netapp-lab-ansible-concord.git
cd netapp-lab-ansible-concord
yes | \cp -rf _bootstrap/CentOS-7-Base.repo /etc/yum.repos.d/CentOS-Base.repo
sudo yum install python3 pip -y
sudo yum install gcc openssl-devel bzip2-devel libffi-devel -y
cd /usr/local/src
wget https://openssl.org/source/openssl-1.1.1k.tar.gz
tar -xzvf openssl-1.1.1k.tar.gz
cd openssl-1.1.1k
autoconf
./config --prefix=/usr/local --openssldir=/etc/ssl --libdir=lib no-shared zlib-dynamic
make
make test
make install
echo "export LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64" >> /etc/profile.d/openssl.sh
source /etc/profile.d/openssl.sh
sudo update-alternatives --install /usr/local/bin/python3 python3 /usr/local/bin/python3.9 1
sudo alternatives --set python3 /usr/local/bin/python3.9
cd .. 
wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
tar -xvf Python-3.9.6.tgz
cd Python-3.9.6
autoconf
./configure --prefix=/usr/local/
sudo make
sudo make altinstall
cd /root/netapp-lab-ansible-concord
python3 -m venv venv
source venv/bin/activate
cd ansible
pip install --upgrade pip setuptools
pip install -r requirements.txt
ansible-galaxy role install -r roles/requirements.yml