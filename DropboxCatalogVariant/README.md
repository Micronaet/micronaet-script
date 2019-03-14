===============
Dropbox Catalog
===============

Start from image folder in different type, ex.:
Image
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

    ---> Video
         > Product1.jpg
         > Product1.001.jpg
         > Product2.jpg
         > Product2.001.jpg

And generate folder in Dropbox with symlinks:

Dropbox 
    ---> PRODUCT1
         > CHROMA.Product1.jpg
         > CHROMA.Product1.001.jpg         
         > ENV.Product1.jpg
         > ENV.Product1.001.jpg         
         > VIDEO.Product1.jpg
         > VIDEO.Product1.001.jpg                           

    ---> PRODUCT2
         > CHROMA.Product2.jpg
         > CHROMA.Product2.001.jpg         
         > ENV.Product2.jpg
         > ENV.Product2.001.jpg         
         > VIDEO.Product2.jpg
         > VIDEO.Product2.001.jpg                                    
         
Config file is: config.py (used dictionary for setup folder and key)
Schedule dropbox.py script every day for symlynk creations

After manage dropbox folder share with link and password

ing. Nicola Riolini
mailto: nicola.riolini@micronaet.com
Micronaet S.r.l.
