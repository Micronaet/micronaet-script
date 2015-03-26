#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import pickle
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
import ConfigParser

# -----------
# Parameters:
# -----------
cfg_file = "openerp.cfg" # same directory
config = ConfigParser.ConfigParser()
config.read(cfg_file)

# General parameters:
force_file = config.get('general', 'force')

# SMTP paramenter for log mail:
smtp_server = config.get('smtp', 'server')
smtp_user = config.get('smtp', 'user')
smtp_password = config.get('smtp', 'password')
smtp_port = int(config.get('smtp', 'port'))
smtp_SSL = eval(config.get('smtp', 'SSL'))
from_addr = config.get('smtp', 'from_addr')

# Mexal parameters:
#mexal_company = config.get('mexal', 'company')
mexal_user = config.get('mexal', 'user')
mexal_password = config.get('mexal', 'password')

# Setup depend on parameter passed (default SDX if not present)
try:
    company = sys.argv[1]
except:
    company = "SDX" # default company

smtp_subject_mask = "%s > %s" % (company, config.get('smtp', 'subject_mask'))

try:
    # Read parameters depend on start up company:
    file_err = config.get(company, 'file_err')             # Log file from mexal (empty = OK, else error)
    mexal_company = config.get(company, 'company')
    to_addr = config.get(company, 'to_addr')
    path_in = config.get(company, 'path_in')               # Folder: in files
    path_out = config.get(company, 'path_out')             # Folder: destination
    path_history = config.get(company, 'path_history')     # Folder: history
    log_file_name = config.get(company, 'log_file_name')
    log_scheduler = config.get(company, 'log_scheduler_name') # Scheduler log file
    sprix_number = int(config.get(company, 'sprix_number'))
    # Jump order too new:
    jump_order_days = eval(config.get(company, 'jump_order_days'))
    left_start_date = int(config.get(company, 'left_start_date'))
    left_days = int(config.get(company, 'left_days'))
except:
    print "[ERR] Chiamata a ditta non presente (scelte possibili: SDX o ELI)"
    sys.exit() # wrong company!

log_file = open(log_file_name, 'a')
log_schedulers_file = open(log_scheduler, 'a')

# -----------------
# Utility function:
# -----------------
# Pickle function:
def store_forced(filename, forced_list):
    ''' Load pickle file in a list that is returned
    '''
    try:
        pickle.dump(forced_list, open(filename, "wb" ) )
        return True
    except:
        return False    

def load_forced(filename):
    ''' Load list of forced from file
    '''
    try:
        res =  pickle.load(open(filename, "rb")) or []
        return res
    except: 
        return []

# Log function:
def log_message(log_file, message, model='info'):
    ''' Write log file and print log file
        log_file: handles of file
        message: text of message
        model: type of message, like: 'info', 'warning', 'error'
    '''
    log_file.write("[%s] %s: %s\n" % (
        model.upper(),
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        message, ))
    print message
    return

def log_scheduler_message(log_file, message):
    ''' Log scheduler information (start stop)
    '''
    log_file.write("%s: %s\n" % (
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        message, ))
    print message
    return

# File function:
def get_timestamp_from_file(file_in, path_in, company="ELI"):
    ''' Get timestamp value from file name
        File is: ELIORD20141103091707.ASC
                 ------YYYYMMGGhhmmss----
        Millisecond are 
            00 for create order ELIORD
            10 for delete order ELICHG     
    '''
    if company == "ELI":
        return "%s-%s-%s %s:%s:%s.%s" % (
            file_in[6:10],   # Year
            file_in[10:12],  # Month
            file_in[12:14],  # Day
            file_in[14:16],  # Hour
            file_in[16:18],  # Minute
            file_in[18:20],  # Second
            "00" if file_in.startswith("ELIORD") else "10" # Millisecond
            )
    else: # company == "SDX":
        return datetime.fromtimestamp(
            os.path.getctime(join(path_in, file_in)))
        

# SMTP function:
def get_smtp(log_message):
    # Start session with SMTP server
    try:
        from smtplib import SMTP
        smtp = SMTP()
        smtp.set_debuglevel(0)
        smtp.connect(smtp_server, smtp_port)
        smtp.login(smtp_user, smtp_password)
        log_message(
            log_file, 
            "Connesso al server %s:%s User: %s Pwd: %s" % (
                smtp_server, smtp_port, smtp_user, smtp_password))
        return smtp
    except:        
        log_message(
            log_file, 
            "Impossibile collegarsi server %s:%s User: %s Pwd: %s" % (
                smtp_server, smtp_port, smtp_user, smtp_password),
            'error', )
        return False

# -----------------------------------------------------------------------------
#                    Program: (NO CHANGE OVER THIS LINE)
# -----------------------------------------------------------------------------
log_scheduler_message(log_schedulers_file, "Start importation [EDI: %s]" % company)

# Mexal parameters:
sprix_command = r"c:\mexal_cli\prog\mxdesk.exe -command=mxrs.exe -a%s -t0 -x2 win32g -p#%s -k%s:%s" % (
    mexal_company, sprix_number, mexal_user, mexal_password)

if datetime.today().weekday() in (3, 4, 5): # TODO (change depend on number of day left)
    left_days += 2
    log_message(log_file, "Aggiunto due giorni extra alla data")

max_date = (datetime.today() + timedelta(days=left_days)).strftime("%Y%m%d")
log_message(log_file, "Valutazione scadenza (salto se >= %s)" % max_date)

# Get list of files and sort before import
file_list = []

try:
    # Sort correctly the files:       
    for file_in in [f for f in listdir(path_in) if isfile(join(path_in, f))]:
        file_list.append(
            (get_timestamp_from_file(file_in, path_in, company), file_in))
    file_list.sort()

    # Print list of sorted files for loggin the operation:
    for ts, file_in in file_list:
        log_message(log_file, "ID: Date: %s\t File: %s" % (
            ts, file_in ))
except:
    log_message(
        log_file, 
        "Impossibile leggere i file da elaborare, script terminato",
        'error', )
    sys.exit()    
       
# Import files sorted
order_imported = ""

for ts, file_in in file_list:    
    # Jump file to delivery in 'left_days' days (usually 3):
    if jump_order_days:
        fin = open(join(path_in, file_in), "r")
        test_date = fin.readline()[left_start_date:left_start_date + 8]
        fin.close()
        
        # Load every time the force list:
        force_list = load_forced(force_file)
        if file_in in force_list:
            force_list.remove(file_in)
            store_forced(force_file, force_list) # TODO if not imported??
            log_message(log_file, "Importazione forzata: %s > %s" % (path_in, file_in))
            
        elif test_date >= max_date:
            log_message(log_file,
                "File saltato [%s] limite %s < data file %s" % (
                    file_in, max_date, test_date), "warning")
            continue
    else:
        test_date = "Data non letta"
    log_message(log_file, "Divisione file: %s > %s" % (path_in, file_in))
    mail_error = "" # reset for every file readed
   
    # Output file parameters (open every loop because closed after import):
    file_out = {
        open(join(path_out, 'ordine.1.txt'), "w"): [0, 2036],
        open(join(path_out, 'ordine.2.txt'), "w"): [2036, 3507], # 1561
        }

    # Remove log file (if present):
    try:
        os.remove(file_err)
    except:
        pass

    # Split input file:
    fin = open(join(path_in, file_in), "r")
    for line in fin:
        position = 0
        for f in file_out:
            f.write("%s\r\n" % (line[
                file_out[f][0] : file_out[f][1]]))

    # Close all file (input and 2 splitted)       
    for f in file_out:
        try:
            f.close()
        except:
            mail_error += "Errore chiudendo file split\n"
    try:       
        fin.close()
    except:
        mail_error += "Errore chiudendo il file di input\n"
   
    # Run mexal:
    #import pdb;pdb.set_trace()
    try:
        comment_err = "Chiamata mexal client"
        os.system(sprix_command)
    
        # Read error file for returned error:
        comment_err = "apertura file"
        f_err = open(file_err, "r")
        comment_err = "lettura file"
        test_err = f_err.read().strip() # ok if work
        comment_err = "test contenuto file"
        if test_err[:2] != "ok":
            comment_err = "test contenuto file ko"
            mail_error += test_err or "Errore generico (non gestito)"
        else:
            comment_err = "test contenuto file ok"
            result = test_err.split(";")
            order_imported += "\tCliente %s - Interno: %s (Scad.: %s\n" % (
                result[1], result[2], test_date)
            log_message(log_file, " Ordine importato: %s" % (result, ))
        comment_err = "chiusura file"    
        f_err.close()
    except:
        mail_error += "Errore generico di importazione (file log non trovato)[%s]!" % comment_err
        pass # No file = no error
       
    if mail_error: # Comunicate
        log_message(
            log_file, "Errore leggendo il file: %s" % mail_error, 'error')

        # Send mail for error (every file):
        smtp = get_smtp(log_message)
        if smtp:    
            smtp.sendmail(
                from_addr, to_addr,
                "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (
                    from_addr, to_addr, smtp_subject_mask % file_in,
                    datetime.now().strftime("%d/%m/%Y %H:%M"), mail_error))
            smtp.quit()       
            log_message(log_file, "Invio mail errore importazione: da %s, a %s, \n\t<<<%s\t>>>" % (
                from_addr, to_addr, mail_error))    
        else:
            log_message(
                log_file, 
                "Mail errore importazione non iviata %s, a %s, \n\t<<<%s\t>>>" % (
                    from_addr, to_addr, mail_error), 'error')   
                    
    else:
        # History the file (only if no error)
        try:
            os.rename(join(path_in, file_in), join(path_history, file_in))
            log_message(
                log_file, "Importato il file e storicizzato: %s" % file_in)
        except:
            log_message(
                log_file, "Errore storicizzando il file: %s" % file_in,
                'error')
            
if order_imported: # Comunicate importation   
    smtp = get_smtp(log_message)
    if smtp:
        smtp.sendmail(
            from_addr, to_addr,
            "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (
                from_addr, to_addr, 'Ordini importati',
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                order_imported))
        smtp.quit()
        log_message(log_file, "Mail ordini importati: da %s, a %s, \n\t<<<%s\t>>>" % (
            from_addr, to_addr, order_imported))
    else:
        log_message(
            log_file, 
            "Mail ordini importati non inviata: da %s, a %s, \n\t<<<%s\t>>>" % (
                from_addr, to_addr, order_imported), "error")
            
log_scheduler_message(log_schedulers_file, "Stop importation [EDI: %s]" % company)

# Close operations:
try:
    log_file.close()    
except:
    pass
try:
    log_scheduler_file.close()    
except:
    pass
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

