#!/bin/sh
##############################################################################
#
#    Copyright (C) 2001-2014 Micronaet SRL (<http://www.micronaet.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
# Installation: copy mount script and create 2 files for server access: 
#
# Command file:
# Start script caller: mount_all.sh # ./mount_centos.sh username
# File: mount_centos.sh
#
# Credentials file:
# File: /root/cifs/zentyal # or  192.168.1.2
# File: /root/cifs/serverwin                                                                                                             
# File: /root/cifs/mexal                                                                                                           

# -------------------------------------------------------------
# Parametri:
# -------------------------------------------------------------
echo "Get user information"
# Linux account:
uid="administrator"
gid="administrator"

# Server name (used also for credentials file name)
server="serverwin" 
zentyal="192.168.1.2"
mexal="192.168.1.110"

root_cred=/root/cifs
server_cred=$root_cred/$server
zentyal_cred=$root_cred/$zentyal
mexal_cred=$root_cred/$mexal

# -----------------------------------------------------------------------------
# Sharing folder path (SMB name):
# -----------------------------------------------------------------------------
# Docnaet:
# TODO change server in zentyal:
docnaet_smb=//$server/centosdocnaet$
docfax_smb=//$server/docfax

# Server:
documenti_smb=//$zentyal/documenti
users_smb=//$zentyal/Users/$1
export_smb=//$mexal/export
scanner_smb=//$zentyal/scanner

# -----------------------------------------------------------------------------
# Mount point path:
# -----------------------------------------------------------------------------
# Root path:
root_mp=/home/$uid/smb

# Docnaet:
docnaet_mp=/docnaet
docfax_mp=$root_mp/docfax

# Server:
documenti_mp=$root_mp/ufficio
users_mp=$root_mp/user
export_mp=$root_mp/estrazioni
scanner_mp=$root_mp/scanner

# -----------------------------------------------------------------------------
# Create mount point:
# -----------------------------------------------------------------------------
# Docnaet folders:
sudo mkdir -p $docnaet_mp
mkdir -p $docfax_mp

# Root share folders:
mkdir -p $root_mp
sudo chown $uid:$gid $root_mp

mkdir -p $documenti_mp
mkdir -p $users_mp
mkdir -p $export_mp
mkdir -p $scanner_mp

# -----------------------------------------------------------------------------
# Connessione share sui mount point:
# -----------------------------------------------------------------------------
# Docnaet:
sudo umount $docnaet_mp
sudo mount -t cifs $docnaet_smb $docnaet_mp -o credentials=$server_cred,gid=$gid,uid=$uid

sudo umount $docfax_mp
sudo mount -t cifs $docfax_smb $docfax_mp -o credentials=$server_cred,gid=$gid,uid=$uid

# Generiche:
sudo umount $documenti_mp
sudo mount -t cifs $documenti_smb $documenti_mp -o credentials=$zentyal_cred,gid=$gid,uid=$uid

sudo umount $user_mp
sudo mount -t cifs $user_smb $user_mp -o credentials=$zentyal_cred,gid=$gid,uid=$uid

sudo umount $export_mp
sudo mount -t cifs $export_smb $export_mp -o credentials=$mexal_cred,gid=$gid,uid=$uid

sudo umount $scanner_mp
sudo mount -t cifs $scanner_smb $scanner_mp -o credentials=$zentyal_cred,gid=$gid,uid=$uid
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
