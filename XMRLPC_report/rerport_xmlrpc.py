import time
import base64
import ConfigParser
import xmlrpclib
import os


cfg_file = os.path.join(os.path.expanduser('openerp.cfg'))
   
# Set up parameters (for connection to Open ERP Database) *********************
config = ConfigParser.ConfigParser()
config.read([cfg_file]) # if file is in home dir add also: , os.path.expanduser('~/.openerp.cfg')])
dbname = config.get('dbaccess', 'dbname')
user = config.get('dbaccess', 'user')
pwd = config.get('dbaccess', 'pwd')
server = config.get('dbaccess', 'server')
port = config.get('dbaccess', 'port')   # verify if it's necessary: getint

uid = 1
printsock = xmlrpclib.ServerProxy(
    'http://192.168.100.174:8069/xmlrpc/report')

ids = [10845]
model = 'sale.order'

id_report = printsock.report(
    dbname, uid, pwd, model, ids, {
        'model': model, 
        'id': ids[0], 
        'report_type': 'aeroo', #'webkit' 'pdf'        
        })
        
state = False
attempt = 0
while not state:
    print 'ID report:', id_report
    report = printsock.report_get(dbname, uid, pwd, id_report)
    state = report['state']
    if not state:
        time.sleep(1)
    attempt += 1
    if attempt > 200:
        print 'Printing aborted, too long delay!'
    if 'result' not in report:
        print 'No report error!'
        continue
        
    string_pdf = base64.decodestring(report['result'])
    file_pdf = open('/home/thebrush/Scrivania/report.pdf', 'w')
    file_pdf.write(string_pdf)
    file_pdf.close()
