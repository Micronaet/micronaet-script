==============================================
Procedure to install script as windows Service
==============================================
To install the service and prepare the environment use script: setup.bat

The script install library:
c:\python27\script\pip.exe pywin32

Update path (permanent):
setx /M PATH "%PATH%;C:\Python27;C:\Python27\Scripts;C:\Python27\Lib\site-packages\pywin32_system32;C:\Python27\Lib\site-packages\win32"

Install service:
c:\python27\python.exe install_service.py install


