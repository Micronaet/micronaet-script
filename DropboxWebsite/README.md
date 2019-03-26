===============
Dropbox Catalog
===============


Copy Album for Wordpress web site selected
Create public structure for 

Start from image folder in different type, ex.:
Album samba folder:
    ---> Chroma
         > Product1.jpg
         > Product1.001.jpg
         > Product2.jpg
         > Product2.001.jpg
         
    ---> Environment
         > Product1.jpg
         > Product1.001.jpg
         > Product2.jpg
         > Product2.001.jpg

And generate folder in Dropbox with symlinks:

Dropbox Public folder / Website:
         > CHROMA.Product1.jpg
         > CHROMA.Product1.001.jpg         
         > ENV.Product1.jpg
         > ENV.Product1.001.jpg         
         > CHROMA.Product2.jpg
         > CHROMA.Product2.001.jpg         
         > ENV.Product2.jpg
         > ENV.Product2.001.jpg         
         
Config file is: config.py (used dictionary for setup folder and key)
Schedule dropbox.py script every day for symlynk creations


ing. Nicola Riolini
mailto: nicola.riolini@micronaet.com
Micronaet S.r.l.
