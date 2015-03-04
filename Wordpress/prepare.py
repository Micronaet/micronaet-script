#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
#                                LIBRARY
# -----------------------------------------------------------------------------
import os
import sys
from datetime import datetime, timedelta
import ConfigParser

# -----------------------------------------------------------------------------
#                              Parameters
# -----------------------------------------------------------------------------
cfg_file = "openerp.cfg" # same directory
config = ConfigParser.ConfigParser()
config.read(cfg_file)

# XML parameters (files to open):
xml_product = config.get('xml', 'product')
xml_availability = config.get('xml', 'availability')
xml_reference = config.get('xml', 'reference')
xml_wordpress = config.get('xml', 'wordpress')

only_available = eval(config.get('xml', 'only_available'))

# Log parameters:
log_log_mail = eval(config.get('log', 'log_mail'))
log_log_verbose = eval(config.get('log', 'log_verbose'))
verbose = eval(config.get('log', 'verbose'))
log_log_return = eval(config.get('log', 'log_return'))

log_log_file = config.get('log', 'log_file') # Log activity
log_log_schedule = config.get('log', 'log_schedule') # Log start / stop event
log_log_err = config.get('log', 'log_err') # Log error
log_log_total = config.get('log', 'log_total') # Log total elements imported

# Remove elements:
remove_product = eval(config.get('remove', 'product'))
#remove_availability = eval(config.get('remove', 'availability'))
#remove_reference = eval(config.get('remove', 'reference'))

#csv
availability_csv = config.get('csv', 'availability') # file csv
availability_mask = config.get('csv', 'availability_mask') + log_log_return
availability_mask = availability_mask.replace("(", "%(")
availability_parameter = eval(config.get('csv', 'availability_parameter')) # param.
availability_title = config.get('csv', 'availability_title') + log_log_return

# SMTP paramenter for log mail:
smtp_server = config.get('smtp', 'server')
smtp_user = config.get('smtp', 'user')
smtp_password = config.get('smtp', 'password')
smtp_port = int(config.get('smtp', 'port'))
smtp_SSL = eval(config.get('smtp', 'SSL'))
smtp_from_addr = config.get('smtp', 'from_addr')
smtp_to_addr = config.get('smtp', 'to_addr')

body = "Esito importazione: %s" % log_log_return
# -----------------------------------------------------------------------------
#                           Utility function
# -----------------------------------------------------------------------------
# Log function:
def log_message(log_file, message, model='info', verbose=True):
    ''' Write log file and print log file
        log_file: handle of file
        message: text of message
        model: type of message, like: 'info', 'warning', 'error'
        verbose: if print out in console 
    '''
    log_file.write("[%s] %s: %s%s" % (
        model.upper(),
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        message, 
        log_log_return,
        ))

    if verbose: # Out on video during importation
        print message
    return

# SMTP function:
def get_smtp():
    ''' Start session with SMTP server
    '''
    try:
        from smtplib import SMTP
        
        smtp = SMTP()
        smtp.set_debuglevel(0)
        smtp.connect(smtp_server, smtp_port)
        smtp.login(smtp_user, smtp_password)
        return smtp
    except:        
        print "Unable to connect to server %s:%s User: %s Pwd: %s" % (
            smtp_server,
            smtp_port,
            smtp_user,
            smtp_password,
            )
        return False

def send_mail(subject, body):
    ''' Send mail for result of importation
    '''
    try:
        smtp = get_smtp()
        if smtp:    
            smtp.sendmail(
                smtp_from_addr, smtp_to_addr,
                "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (
                    smtp_from_addr, smtp_to_addr, subject,
                    datetime.now().strftime("%d/%m/%Y %H:%M"), 
                    body))
            smtp.quit()       
    except:
        print sys.exc_info()        

# -----------------------------------------------------------------------------
#                                    MAIN
# -----------------------------------------------------------------------------
error_alert = False # test at the end if one error occurred

try:
    # -------------------------------------------------------------------------
    #                              LOG FILES:
    # -------------------------------------------------------------------------
    error = "Error opening log files:"
    
    # Open log files:
    log_file = open(log_log_file, 'a')
    log_schedule = open(log_log_schedule, 'a')
    log_err = open(log_log_err, 'a')
    log_total = open(log_log_total, 'a')

    # Log events:
    log_message(
        log_schedule, 
        "Start conversion", )

    log_message(
        log_file, 
        "Open log files", )

    # -------------------------------------------------------------------------
    #                              CONVERSION
    # -------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------
    # Availability
    # -------------------------------------------------------------------------
    error = "Error importing availability"
    log_message(
        log_file, 
        "Start availability xml file", )

    availability = {}
    i = 0 # line counter
    tot = 0 # record counter
    start = False # find one record
    item_id = False # find id record
    record = "" # text of element
    
    # Extra csv file:
    availability_csv_file = open(availability_csv, 'w')
    availability_csv_file.write(availability_title)
    line_csv = dict.fromkeys(availability_parameter, '')
    for line in open(xml_availability, 'r'):
        i += 1
        if i <= 2: # Jump first 2 line
            continue
            
        if not start and "<Disponibilita>" in line:
            start = True
            continue
            
        if start and not item_id:
            if "ID_ARTICOLO" in line:
                item_id = line.split(
                    "<ID_ARTICOLO>")[-1].split(
                        "</ID_ARTICOLO>")[0]
            else:
                error_alert = True
                log_message(
                    log_err, 
                    "Availability: not found ID_ARTICOLO [line: %s]" % i, )
            continue

        # Extra export: Check element for CSV file:
        for csv_key in availability_parameter:
            if csv_key in line:
                line_csv[csv_key] = line.split(
                    "<%s>" % csv_key)[-1].split(
                        "</%s>" % csv_key)[0]
        
        if start and "</Disponibilita>" in line:
            # Extra export CSV file:
            # Write CSV line and reset dict
            availability_csv_file.write(
                availability_mask % (line_csv))
            line_csv = (dict.fromkeys(availability_parameter, ''))
                
            
            if item_id not in availability:
                availability[item_id] = []
            availability[item_id].append(record)
            tot += 1

            if verbose:
                print "%s. Record availability for: %s" % (
                    tot,
                    item_id, 
                    )

            start = False
            item_id = False
            record = ""
            continue
        
        if start:
            record += line    
    
    msg = "File: %s Line: %s Record: %s Products: %s" % (
        xml_availability,
        i,
        tot,
        len(availability),
        )
    body += msg + log_log_return    
    log_message(
        log_total, 
        msg,
        )

    # -------------------------------------------------------------------------
    # Reference
    # -------------------------------------------------------------------------
    error = "Error importing reference"
    log_message(
        log_file, 
        "Start reference xml file", )

    reference = {}
    i = 0 # line counter
    tot = 0 # record counter
    start = False # find one record
    item_id = False # find id record
    record = "" # text of element
    
    for line in open(xml_reference, 'r'):
        i += 1
        if i <= 2: # Jump first 2 line
            continue
            
        if not start and "<Riferimenti>" in line:
            start = True
            continue
            
        if start and not item_id:
            if "RF_RECORD_ID" in line:
                item_id = line.split(
                    "<RF_RECORD_ID>")[-1].split(
                        "</RF_RECORD_ID>")[0]
            else:
                error_alert = True
                log_message(
                    log_err, 
                    "Reference: not found ID_ARTICOLO [line: %s]" % i, )
            continue

        if start and "</Riferimenti>" in line:
            if item_id not in reference:
                reference[item_id] = []
            reference[item_id].append(record)
            tot += 1

            if verbose:
                print "%s. Record reference for: %s" % (
                    tot,
                    item_id, 
                    )
            start = False
            item_id = False
            record = ""
            continue
        
        if start:
            record += line    

    msg = "File: %s Line: %s Record: %s Products: %s" % (
        xml_reference,
        i,
        tot,
        len(reference), )
    body += msg + log_log_return    
    log_message(
        log_total, 
        msg, 
        )
    
    # -------------------------------------------------------------------------
    # Product
    # -------------------------------------------------------------------------
    error = "Error importing availability"
    log_message(
        log_file, 
        "Start product xml file", )

    i = 0 # line counter
    tot = 0 # record counter
    start = False # find one record
    item_id = False # find id record
    jump = False
    deleted = False # CANCELLATO
    gender = False
    
    file_wordpress = open(xml_wordpress, 'w') # output file

    # Start file:
    file_wordpress.write("""<?xml version="1.0" standalone="yes"?>
<DocumentElement Date="2014-11-25 15:48:15">
  <Prodotti>""")
    
    for line in open(xml_product, 'r'):
        try:
            error = "Error start loop"
            i += 1
            # -----------------------------------------------------------------
            # Jump first 2 line
            # -----------------------------------------------------------------
            if i <= 2: 
                continue
                
            error = "Error test start prodotti"
            if not start and "<Prodotti>" in line:
                start = True
                continue
                
            error = "Error read id"
            # -----------------------------------------------------------------
            # 1st line after prodotti
            # -----------------------------------------------------------------
            if start and not item_id: 
                if "ID_ARTICOLO" in line:
                    item_id = line.split(
                        "<ID_ARTICOLO>")[-1].split(
                            "</ID_ARTICOLO>")[0]                            
                else:
                    error = True
                    log_message(
                        log_err, 
                        "Prodotto: ID_ARTICOLO non trovato [line: %s]" % i, )
                    jump = True
                    continue

                # Check only available
                if only_available and item_id not in availability:                    
                    jump = True
                else:
                    # Write prodotto start tag:
                    file_wordpress.write("%s   <Prodotto>%s" % (
                        log_log_return,
                        log_log_return,
                        ))
                        
                    file_wordpress.write(line) # ID_ARTICOLO
                continue

            # -----------------------------------------------------------------
            # End record
            # -----------------------------------------------------------------
            error = "Error check close prodotti"
            if start and "</Prodotti>" in line: 
                reference_tot = 0
                availability_tot = 0
                if not jump:
                    # ---------------------------------------------------------
                    # Write reference:
                    # ---------------------------------------------------------
                    error = "Error write reference"
                    if item_id in reference:
                        file_wordpress.write("    <Immagini>")                
                        reference_tot = len(reference[item_id])
                        for item in reference[item_id]:
                            file_wordpress.write(
                                "%s     <Riferimenti>%s%s     </Riferimenti>" % (
                                    log_log_return,
                                    log_log_return,
                                    item.replace(" "*4, " "*6),
                                    ))
                                    
                        file_wordpress.write("%s    </Immagini>%s" % (
                            log_log_return,
                            log_log_return,
                            ))
                    else:
                        file_wordpress.write("    <Immagini></Immagini>%s" % log_log_return)
                    
                    # ---------------------------------------------------------
                    # Write availability:
                    # ---------------------------------------------------------
                    error = "Error write availability"
                    if item_id in availability:
                        file_wordpress.write("    <Disponibilita>%s" % log_log_return)                
                        availability_tot = len(availability[item_id])
                        for item in availability[item_id]:
                            file_wordpress.write(
                                "     <Disponibilita>%s%s     </Disponibilita>%s" % (
                                    log_log_return,
                                    item.replace(" "*4, " "*6),
                                    log_log_return,
                                    ))
                        file_wordpress.write("    </Disponibilita>")
                    else:
                        file_wordpress.write(
                            "    <Disponibilita></Disponibilita>")
                    
                    file_wordpress.write("%s   </Prodotto>" % log_log_return)
                tot += 1

                error = "End part"
                if verbose:
                    body += "%s. Prodotto %s: %s [Dispo: %s - Immagini: %s (%s)]%s" % (
                        tot,
                        "saltato" if jump else "creato",
                        item_id, 
                        availability_tot,
                        reference_tot,
                        "outofstock" if deleted else "instock",
                        log_log_return,
                        )
                # Reset variables for next record:        
                start = False
                item_id = False
                jump = False
                gender = False
                record = ""
                continue
            
            if start and not jump:
                # -------------------------------------------------------------
                # Particular cases for substitution key:
                # -------------------------------------------------------------
                # A) Precancelled record:
                writeline = True
                if "<CANCELLATO>" in line:
                    writeline = False
                    deleted = ">1<" in line
                    if deleted:
                        file_wordpress.write(
                            "    <VALIDO>outofstock</VALIDO>%s" % log_log_return)    
                    else: # "0"
                        file_wordpress.write(
                            "    <VALIDO>instock</VALIDO>%s" % log_log_return)    
                
                # B1) Gender - SETTORE:
                if "<SETTORE />" in line:
                    gender = "Unisex"                
                elif "<SETTORE>" in line:
                    writeline = False
                    # Case: Donna Uomo Unisex Bambino
                    gender = line.split("<SETTORE>")[-1].split("</SETTORE>")[0]
                    # No write!
                    
                # B2) Gender - GRUPPO:
                if "<GRUPPO>" in line:
                    writeline = False
                    group = line.split("<GRUPPO>")[-1].split("</GRUPPO>")[0]
                    if gender in ("Donna", "Uomo", "Bambino"):
                        group = "%s > %s" % (
                            gender,
                            group,
                            )
                    elif gender == "Unisex":
                        group = "Uomo > %s | Donna > %s" % (
                            group,
                            group,
                            )
                    else: # Case not managed
                        log_message(
                            log_err, 
                            "%s. Error gender not found: %s!" % (
                                i,
                                gender, ))
                                
                    file_wordpress.write(
                        "    <GRUPPO>%s</GRUPPO>%s" % (
                            group,
                            log_log_return,
                            ))
                            
                # -------------------------------------------------------------
                # Particular cases jumped jeys:
                # -------------------------------------------------------------
                for remove_key in remove_product:
                    if remove_key in line:
                        writeline = False
                        break # stop loop                   
                
                # -------------------------------------------------------------
                # END) Common part:            
                # -------------------------------------------------------------
                if writeline: # test if need to write:
                    file_wordpress.write(line)
                    
        except:
            print error, sys.exc_info() # TODO
            
    # Start file:
    file_wordpress.write("""
 </Prodotti> 
</DocumentElement>""")

    msg = "File: %s Line: %s Record: %s" % (
        xml_product,
        i,
        tot, )
    body += msg + log_log_return    
    log_message(
        log_total, 
        msg,
        )

    # -------------------------------------------------------------------------
    #                             FTP OPERATIONS:
    # -------------------------------------------------------------------------
    #os.system(sprix_command)

    # -------------------------------------------------------------------------
    #                             HISTORY OPERATIONS:
    # -------------------------------------------------------------------------
    # History the file (only if no error)
    """try:
        os.rename(join(path_in, file_in), join(path_history, file_in))
        log_message(
            log_file, "Importato il file e storicizzato: %s" % file_in)
    except:
        log_message(
            log_file, "Errore storicizzando il file: %s" % file_in,
            'error')"""

except:
    print "[ERR] %s [%s]" % (error, sys.exc_info())    
    sys.exit() 

# -----------------------------------------------------------------------------
#                                 Close operations:
# -----------------------------------------------------------------------------
log_message(
    log_schedule, 
    "End conversion", )

try:
    log_schedule.close()    
except:
    log_message(
        log_file, 
        "Error closing schedule file: " % log_log_schedule, 
        model='error', )

try:
    log_err.close()    
except:
    log_message(
        log_file, 
        "Error closing err file: " % log_err_file, 
        model='error', )

try:
    log_total.close()    
except:
    log_message(
        log_file, 
        "Error closing total file: " % log_total_file, 
        model='error', )

try:
    log_file.close()    
except:
    pass

if error_alert:
    send_mail(
        "Errore convertendo i file!", 
        "Errore durante la conversione file")
    print "Errore nelle conversioni consultare i log:", log_err_file
else:
    send_mail(
        "Conversione corretta!", 
        body, )
    print "Procedura terminata correttamente"
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
