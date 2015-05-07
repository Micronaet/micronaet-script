import os
import sys
from datetime import datetime

f = open('c:\\Micronaet\docnaet.log', 'a')
    
extra_path = sys.argv[1].split(":")
if extra_path[0] == 'docnaet':
    static_path = "\\\\mexal\\doc_doc$\\"
else:    
    static_path = "\\\\mexal\\lab_doc$\\"
    
filename = static_path + extra_path[-1][2:-1].replace("\\\\", "\\")
os.system("start " + filename)

f.write("%s: %s\n" % (datetime.now(), filename))
f.close()
