import getpass
import platform
import sys

# -----------------------------------------------------------------------------
#                                Parameters
# -----------------------------------------------------------------------------
mysql_host = '192.168.21.251'
mysql_user = 'loguser'
mysql_password = 'loguser'
mysql_db = 'lognaet'
# -----------------------------------------------------------------------------

if len(sys.argv) == 6:    
    pass # TODO Error wrong list of argument:    
    
connection = MySQLdb.connect(
    host=mysql_host, 
    user=mysql_user,
    passwd=mysql_password,
    db=mysql_db,
    )
cr = connection.cursor()

cr.execute("""
    INSERT 
        INTO Logs (
            LogHostname, LogUserName, LogDescrizione, logData, logRighe, 
            logOraInizio, logOraFine, logTipo) 
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" )
    """ % (
        platform.node(), # computer name
        getpass.getuser(), # user name
        "Data %s: %s, dalle %s alle %s, Righe: %s" % (
            sys.argv[1], # type
            sys.argv[2], # account date
            sys.argv[4], # start time
            sys.argv[5], # stop time
            sys.argv[3], # number of row
            ),
        sys.argv[2], # account date
        sys.argv[3], # number of row
        sys.argv[4], # start time
        sys.argv[5], # stop time
        sys.argv[1], # type
        ))

connection.close()
    
    


    

    






