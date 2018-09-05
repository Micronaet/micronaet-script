echo Install dependency:
c:\python27\script\pip.exe pywin32

echo Update percorso di default:
setx /M PATH "%PATH%;C:\Python27;C:\Python27\Scripts;C:\Python27\Lib\site-packages\pywin32_system32;C:\Python27\Lib\site-packages\win32"

echo Install service:
cd "C:\Users\glori\Dropbox\git\WindowsService"
c:\python27\python.exe install_service.py install

pause
