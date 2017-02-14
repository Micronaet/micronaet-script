#!/bin/bash
# Parameters:
origin="192.168.100.121"

# Update system and install dependencies:
echo Installazione dipendenze: ************************************************
apt-get update; apt-get upgrade

apt-get install postgresql pgadmin3 openssh-server python-dateutil python-decorator python-docutils python-feedparser \
python-gdata python-gevent python-imaging python-jinja2 python-ldap python-libxslt1 python-lxml \
python-mako python-mock python-openid python-passlib python-psutil python-psycopg2 python-pybabel \
python-pychart python-pydot python-pyparsing python-pypdf python-reportlab python-requests \
python-simplejson python-tz python-unittest2 python-vatnumber python-vobject python-werkzeug \
python-xlwt python-yaml wkhtmltopdf python-yaml node-less git

# Create user for ODOO:
echo Creazione utenti: ********************************************************
#adduser administrator
adduser odoo #--system --home=/home/odoo --group odoo

# Installazione postgres:
echo Configurazione postgres: *************************************************
#sudo nano /etc/postgresql/x.x/main/pg_hba.conf 
#local   all         odoo                              md5
service postgresql restart

# Comandi eseguiti come posgtres
sudo su -c "createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt odoo" -s postgres
#createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt odoo

# Copia files
echo Copia files: *************************************************************
#scp -rv administrator@$origin:/home/administrator/lp /home/administrator/
scp -rv root@$origin:/home/administrator/photo /home/administrator/
#scp -rv administrator@$origin:/home/administrator/ETL /home/administrator/
#scp -rv administrator@$origin:/home/administrator/git /home/administrator/
chown administrator:administrator /home/administrator

scp -rv administrator@$origin:/home/odoo/ /home/odoo
chown odoo:odoo /home/odoo -R

# Copia servizio:
echo Copia servizio: **********************************************************
scp root@$origin:/etc/init.d/odoo-server /etc/init.d/odoo-server
chmod 755 /etc/init.d/odoo-server
chown root: /etc/init.d/odoo-server

scp root@$origin:/etc/odoo-server.conf /etc/odoo-server.conf
chown odoo: /etc/odoo-server.conf
chmod 640 /etc/odoo-server.conf
update-rc.d odoo-server defaults

# Setup cartelle temporanee:
echo Setup cartelle temporanee:
mkdir /var/log/odoo
chown odoo:root /var/log/odoo

# Parte extra debian:
echo Installazione node-less per debian: **************************************
apt-get install build-essential libssl-dev curl git-core
mkdir /root/Scaricati
cd /root/Scaricati
wget http://nodejs.org/dist/v0.12.0/node-v0.12.0.tar.gz
tar xvzf node-v0.12.0.tar.gz
cd node-v0.12.0
./configure
make
make install
npm install -g less

# pip install:
wget https://bootstrap.pypa.io/get-pip.py
python ./get-pip.py
pip install pip==8.1.2

# Smb share to create
echo Creazione condivisioni samba: ********************************************
apt-get install samba cifs-utils

pip install psycogreen
pip install pysftp # da errore per paramiko

echo Ricordare configurazione file postgres
echo Mettere sudoers odoo e administrator


# Da mettere a posto:
sudo apt-get install build-essential libssl-dev libffi-dev python-dev

cd /aeolib
sudo python ./setup.py install
sudo pip install erppeek
sudo pip install qrcode
sudo pip install xlrd
sudo pip install xlsxwriter
sudo pip install dbf


lanciare ~/update_git.sh

