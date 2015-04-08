#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
#                                LIBRARY
# -----------------------------------------------------------------------------
import os
import sys
import glob
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
xml_pricelist = config.get('xml', 'pricelist')
xml_wordpress = config.get('xml', 'wordpress')

# Path for update files:
#path_product = os.path.dirname(xml_product)
path_availability = os.path.dirname(xml_product)
path_reference = os.path.dirname(xml_product)
path_pricelist = os.path.dirname(xml_product)

# Filter mask for update:
#xml_product_filter = config.get('xml', 'product_filter')
xml_availability_filter = config.get('xml', 'availability_filter')
#xml_reference_filter = config.get('xml', 'reference_filter')
#xml_pricelist_filter = config.get('xml', 'pricelist_filter')

only_available = eval(config.get('xml', 'only_available'))

# Log parameters:
log_log_mail = eval(config.get('log', 'log_mail'))
log_log_verbose = eval(config.get('log', 'log_verbose'))
verbose = eval(config.get('log', 'verbose'))
cr = eval(config.get('log', 'log_return'))

log_log_file = config.get('log', 'log_file') # Log activity
log_log_schedule = config.get('log', 'log_schedule') # Log start / stop event
log_log_err = config.get('log', 'log_err') # Log error
log_log_total = config.get('log', 'log_total') # Log total elements imported

# Remove elements:
remove_product = eval(config.get('remove', 'product'))

#csv:
output_csv = config.get('csv', 'output') # file csv
product_field_text = config.get('csv', 'product_fields')
product_fields_csv = product_field_text.split("|")
product_mask = eval(config.get('csv', 'product_mask')).replace("*", "%")
# Create replace dict:
product_replace_csv = eval(config.get('csv', 'product_replace')).split("|")
product_replace = {}
pos = 0
for element in product_replace_csv:
    if element:
        product_replace[product_fields_csv[pos]] = element
    pos += 1

availability_field_text = config.get('csv', 'availability_fields')
availability_fields_csv = availability_field_text.split("|")
availability_mask = eval(config.get('csv', 'availability_mask')).replace("*", "%")
# Create replace dict:
availability_replace_csv = eval(
    config.get('csv', 'availability_replace')).split("|")
availability_replace = {}
pos = 0
for element in availability_replace_csv:
    if element:
        availability_replace[availability_fields[pos]] = element
    pos += 1

# Read start up parameter (for update mode):
if len(sys.argv) == 2 and sys.argv[1].lower() == 'update':    
    update_mode = True
else:
    update_mode = False    
    

# SMTP paramenter for log mail:
smtp_server = config.get('smtp', 'server')
smtp_user = config.get('smtp', 'user')
smtp_password = config.get('smtp', 'password')
smtp_port = int(config.get('smtp', 'port'))
smtp_SSL = eval(config.get('smtp', 'SSL'))
smtp_from_addr = config.get('smtp', 'from_addr')
smtp_to_addr = config.get('smtp', 'to_addr')

body = "Esito importazione: %s" % cr
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
        cr,
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
    # In update mode search last:
    if update_mode: # search last dated file for open        
        error = "Error importing availability update"
        try:
            file_list = glob.glob(os.path.join(
                path_availability, xml_availability_filter))
            file_list.sort()    
            xml_availability = file_list[-1]
        except:
            log_message(
                log_file,
                "Error reading availability data file (use complete file)!", )
    else:
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

    availability_csv = {}
    for line in open(xml_availability, 'r'):
        i += 1
        if i <= 2: # Jump first 2 line
            continue
            
        if not start and "<Disponibilita>" in line:
            start = True
            continue
            
        # ----------------    
        # Extra CSV export
        # ----------------
        for csv_key in availability_fields_csv:
            if csv_key in line:
                key = line.split(
                    "<%s>" % csv_key)[-1].split(
                        "</%s>" % csv_key)[0]
                        
                # csv construction:
                if csv_key in availability_replace:
                    key = key.replace(
                        availability_replace(csv_key)[0], 
                        availability_replace(csv_key)[1],
                        )
                availability_temp[csv_key] = key

        if start and not item_id:
            if "ID_ARTICOLO" in line:
                item_id = line.split(
                    "<ID_ARTICOLO>")[-1].split(
                        "</ID_ARTICOLO>")[0]                        
                        
                # csv reset: 
                if item_id not in availability_csv:
                    availability_csv[item_id] = []
                availability_temp = dict.fromkeys(availability_fields_csv, '')    
                
            else:
                error_alert = True
                log_message(
                    log_err, 
                    "Availability: not found ID_ARTICOLO [line: %s]" % i, )
            continue
        
        if start and "</Disponibilita>" in line:
            if item_id not in availability:
                availability[item_id] = []
            availability[item_id].append(record)
            tot += 1
            
            # csv append record
            availability_csv[item_id].append(availability_temp)

            if verbose:
                print "%s. Record availability for: %s" % (
                    tot, item_id, )

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
    body += msg + cr    
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
    body += msg + cr    
    log_message(
        log_total, 
        msg, 
        )

    # -------------------------------------------------------------------------
    # Pricelist
    # -------------------------------------------------------------------------
    error = "Error importing pricelist"
    log_message(
        log_file, 
        "Start pricelist xml file", )

    pricelist = {}
    i = 0 # line counter
    tot = 0 # record counter
    start = False # find one record
    item_id = False # find id record
    record = "" # text of element

    for line in open(xml_pricelist, 'r'):
        i += 1
        if i <= 2: # Jump first 2 line
            continue
            
        if not start and "<LISTINI>" in line:
            start = True
            continue
            
        if start and not item_id:
            if "LI_ID_VARIANTI" in line:
                item_id = line.split(
                    "<LI_ID_VARIANTI>")[-1].split(
                        "</LI_ID_VARIANTI>")[0]
            else:
                error_alert = True
                log_message(
                    log_err, 
                    "Pricelist: not found LI_ID_VARIANTI [line: %s]" % i, )
            continue

        if start and "</LISTINI>" in line:
            if item_id not in pricelist:
                pricelist[item_id] = []
            pricelist[item_id].append(record)
            tot += 1

            if verbose:
                print "%s. Record pricelist for: %s" % (
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
        xml_pricelist,
        i,
        tot,
        len(pricelist), )
    body += msg + cr    
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
    
    # csv collector:
    product_csv = {}    
    for line in open(xml_product, 'r'):
        try:
            error = "Error start loop"
            i += 1
            # -----------------------------------------------------------------
            # Jump first 2 line (or empty line)
            # -----------------------------------------------------------------
            if i <= 2 or not line.strip(): 
                continue

            error = "Error test start prodotti"
            if not start and "<Prodotti>" in line:
                start = True
                continue
                
            # ----------------    
            # Extra CSV export
            # ----------------
            for csv_key in product_fields_csv:             
                if csv_key in line:
                    key = line.split(
                        "<%s>" % csv_key)[-1].split(
                            "</%s>" % csv_key)[0]
                            
                    if csv_key in product_replace:
                        key = key.replace(
                            product_replace[csv_key][0], 
                            product_replace[csv_key][1],
                            )
                    # csv construction record       
                    product_csv[item_id][csv_key] = key

            error = "Error read id"
            # -----------------------------------------------------------------
            # 1st line after prodotti
            # -----------------------------------------------------------------
            if start and not item_id: 
                if "ID_ARTICOLO" in line:
                    item_id = line.split(
                        "<ID_ARTICOLO>")[-1].split(
                            "</ID_ARTICOLO>")[0]                            
                    
                    # csv reset (always not present!):  
                    product_csv[item_id] = dict.fromkeys(
                        product_fields_csv, '')
                    product_csv[item_id]['ID_ARTICOLO'] = item_id # add key
                        
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
                        cr,
                        cr,
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
                pricelist_tot = 0
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
                                    cr,
                                    cr,
                                    item.replace(" "*4, " "*6),
                                    ))
                                    
                        file_wordpress.write("%s    </Immagini>%s" % (
                            cr,
                            cr,
                            ))
                    else:
                        file_wordpress.write("    <Immagini></Immagini>%s" % cr)
                    
                    # ---------------------------------------------------------
                    # Write availability:
                    # ---------------------------------------------------------
                    error = "Error write availability"
                    if item_id in availability:
                        file_wordpress.write("    <Disponibilita>%s" % cr)                
                        availability_tot = len(availability[item_id])
                        for item in availability[item_id]:
                            file_wordpress.write(
                                "     <Disponibilita>%s%s     </Disponibilita>%s" % (
                                    cr,
                                    item.replace(" "*4, " "*6),
                                    cr,
                                    ))
                        file_wordpress.write("    </Disponibilita>")
                    else:
                        file_wordpress.write(
                            "    <Disponibilita></Disponibilita>")

                    # ---------------------------------------------------------
                    # Write pricelist:
                    # ---------------------------------------------------------
                    error = "Error write pricelist"
                    if item_id in pricelist:
                        file_wordpress.write(
                            "%s    <Listini>" % cr)
                        pricelist_tot = len(pricelist[item_id])
                        for item in pricelist[item_id]:
                            file_wordpress.write(
                                "%s     <Listini>%s%s     </Listini>" % (
                                    cr,
                                    cr,
                                    item.replace(" "*4, " "*6),
                                    #cr,
                                    ))
                        file_wordpress.write(
                            "%s    </Listini>" % cr)
                    else:
                        file_wordpress.write(
                            "%s    <Listini></Listini>" % cr)
                    
                    file_wordpress.write("%s   </Prodotto>" % cr)
                tot += 1

                error = "End part"
                if verbose:
                    body += "%s. Prodotto %s: %s [Dispo: %s - Immagini: %s - Listino: %s (%s)]%s" % (
                        tot,
                        "saltato" if jump else "creato",
                        item_id, 
                        availability_tot,
                        reference_tot,
                        pricelist_tot,
                        "outofstock" if deleted else "instock",
                        cr,
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
                            "    <VALIDO>outofstock</VALIDO>%s" % cr)    
                    else: # "0"
                        file_wordpress.write(
                            "    <VALIDO>instock</VALIDO>%s" % cr)    
                
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
                            cr,
                            ))
                            
                # -------------------------------------------------------------
                # Particular cases jumped jeys:
                # -------------------------------------------------------------
                for remove_key in remove_product:
                    # 3 cases: "<key>" "<key " "</key>" (problema con tag + attr)
                    if (
                            "<%s>" % remove_key in line or 
                            "<%s " % remove_key in line or 
                            "</%s>" % remove_key in line):
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
    body += msg + cr    
    log_message(
        log_total, 
        msg,
        )

    # -------------------------------------------------------------------------
    #                            CREATE CSV FILE:
    # -------------------------------------------------------------------------
    # ---------------
    # Extra csv file:
    # ---------------
    output_csv_file = open(output_csv, 'w')
     
    # Loop for all product linking availability    
    for k1 in product_csv:
        for item in availability_csv.get(k1, []):
            ris = "%s%s%s" % (
                product_mask % product_csv[k1],
                availability_mask % item,
                cr)
            output_csv_file.write(ris)

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
