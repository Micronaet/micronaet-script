import getpass
import platform
import sys
import MySQLdb
from datetime import datetime

# -----------------------------------------------------------------------------
#                                Parameters
# -----------------------------------------------------------------------------
mysql_host = '192.168.21.251'
mysql_user = 'loguser'
mysql_password = 'loguser'
mysql_db = 'lognaet'

mm_file = 'c:\zc.txt'
# -----------------------------------------------------------------------------

connection = MySQLdb.connect(
    host=mysql_host, 
    user=mysql_user,
    passwd=mysql_password,
    db=mysql_db,
    )
cr = connection.cursor()

for row in open(mm_file, 'r'): # loop on all rows
    cr.execute("""
        INSERT INTO LogMM (
            logLotto, logCausale, logHN,logUserName, logDoc, logSerie,
            logCodiceArt, logNumero, logContoCF, logData, logAnno, 
            logTS, logPrecedente, logAttuale) 
        VALUES (
            '%s', '%s', '%s', '%s', '%s', %s, '%s', %s, '%s', '%s', %s, 
            '%s','%s','%s');"
        """ % (
            row[11:16].replace(chr(0), ''), # Lot
            row[16:18].replace(chr(0), ''), # Cause: 
            # 01 Del, 02 Var(Q), 03 Var(P.), 04 Var(Disc), 05 Add
                        
            platform.node(), # computer name
            getpass.getuser(), # user name
            row[58:60].replace(chr(0), ''), # Type of doc
            row[16:18].replace(chr(0), ''), # Document
            row[66:67].replace(chr(0), ''), # Serial
            row[:16].replace(chr(0), ''), # ID article
            row[60:66].replace(chr(0), ''), # Number
            row[67:69].replace(chr(0), ''), # Fiscal code
            row[79:87].replace(chr(0), ''), # Date
            row[75:79].replace(chr(0), ''), # Year
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),# Timestamp
            row[18:38].replace(chr(0), ''), # Previous
            row[38:58].replace(chr(0), ''), # Current
            ))
connection.close()

# Remove file:    
os.delete(mm_file)
