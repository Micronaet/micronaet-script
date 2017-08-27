#!/bin/bash
# Parameters:
origin="192.168.100.121"

# Update system and install dependencies:
echo Installazione dipendenze: ************************************************
apt-get update; apt-get upgrade

apt-get install postgresql pgadmin3 openssh-server python-dateutil \
    python-decorator python-docutils python-feedparser \
    python-gdata python-gevent python-imaging python-jinja2 python-ldap \
    python-libxslt1 python-lxml \
    python-mako python-mock python-openid python-passlib python-psutil \
    python-psycopg2 python-pybabel \
    python-pychart python-pydot python-pyparsing python-pypdf \
    python-reportlab python-requests \
    python-simplejson python-tz python-unittest2 python-vatnumber \
    python-vobject python-werkzeug \
    python-xlwt python-yaml wkhtmltopdf python-yaml node-less git \
    build-essential libssl-dev libffi-dev python-dev \
    python-pyodbc screen python-mysqldb


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
pip install pip==8.1.2 # XXX se necessario
pip install psycogreen pysftp erppeek qrcode xlrd xlsxwriter dbf sqlalchemy \
    codicefiscale unicodecsv pymssql

# Non si installano: unixodbc pyodbc
# Smb share to create
echo Creazione condivisioni samba: ********************************************
apt-get install samba cifs-utils

cd ~/git/aeroolib 
python ./setup.py install

echo Ricordare configurazione file postgres
echo Mettere sudoers odoo e administrator

echo Aggiorno moduli:
#~/update_git.sh # integarlo qui magari
cd ~/mx/
cd account-financial-tools
git pull
cd ../micronaet
git pull
cd ../micronaet-accounting
git pull
cd ../micronaet-analytic
git pull
cd ../micronaet-bom
git pull
cd ../micronaet-campaign
git pull
cd ../micronaet-crm
git pull
cd ../micronaet-developer
git pull
cd ../micronaet-email
git pull
cd ../micronaet-force
git pull
cd ../micronaet-hr
git pull
cd ../micronaet-images
git pull
cd ../micronaet-label
git pull
cd ../micronaet-menu
git pull
cd ../micronaet-migration
git pull
cd ../micronaet-mx
git pull
cd ../micronaet-mx8
git pull
cd ../micronaet-note-alert
git pull
cd ../micronaet-notify
git pull
cd ../micronaet-order
git pull
cd ../micronaet-product
git pull
cd ../micronaet-production
git pull
cd ../micronaet-purchase
git pull
cd ../micronaet-sale
git pull
cd ../micronaet-sql
git pull
cd ../micronaet-sql7
git pull
cd ../micronaet-utility
git pull
cd ../micronaet-xmlrpc
git pull
cd ..

echo scarico moduli nuovi:
git clone https://www.github.com/Micronaet/micronaet-connector
git clone https://www.github.com/Micronaet/micronaet-php-web

echo Ricreo i collegamenti simbolici:
cd ~/git/addons
ln -s ~/mx/account-financial-tools/* .
ln -s ~/mx/micronaet/* .
ln -s ~/mx/micronaet-accounting/* .
ln -s ~/mx/micronaet-analytic/* .
ln -s ~/mx/micronaet-bom/* .
ln -s ~/mx/micronaet-campaign/* .
ln -s ~/mx/micronaet-crm/* .
ln -s ~/mx/micronaet-connector/* .
ln -s ~/mx/micronaet-developer/* .
ln -s ~/mx/micronaet-email/* .
ln -s ~/mx/micronaet-force/* .
ln -s ~/mx/micronaet-hr/* .
ln -s ~/mx/micronaet-images/* .
ln -s ~/mx/micronaet-label/* .
ln -s ~/mx/micronaet-menu/* .
ln -s ~/mx/micronaet-migration/* .
ln -s ~/mx/micronaet-mx/* .
ln -s ~/mx/micronaet-mx8/* .
ln -s ~/mx/micronaet-note-alert/* .
ln -s ~/mx/micronaet-notify/* .
ln -s ~/mx/micronaet-order/* .
ln -s ~/mx/micronaet-php-web/* .
ln -s ~/mx/micronaet-product/* .
ln -s ~/mx/micronaet-production/* .
ln -s ~/mx/micronaet-purchase/* .
ln -s ~/mx/micronaet-sale/* .
ln -s ~/mx/micronaet-sql/* .
# valutare: ln -s ~/mx/micronaet-sql7/* .
ln -s ~/mx/micronaet-utility/* .
ln -s ~/mx/micronaet-xmlrpc/* .



echo Fare script per inserire tutti i collegamenti simbolici (occhio alle cartelle c\'è netsvc in parecchi moduli)

echo backup e restore database
echo fare una rilevazione dei moduli nuovi
echo fare l\'update all

#Note: 
# Riscaricato micronaet-menuitem
# Manca rep: micronaet-connector
# Problema con module bom_dynamic_structured << min_optional (campo non esistente!)

