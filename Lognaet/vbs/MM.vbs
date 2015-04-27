dim WshShell, FileShell
dim logLotto,logHN,logUserName,logPrecedente, logAttuale, logID_articolo,logCausale,logTipoDoc,logSerie,logNumero,logCF,logSconto,logQ,logPrezzo,logData,logAnno,logTS
dim FileMM, login

' Inizializzazioni:
FileMM="c:\zc.txt"
'login="Utente=Administrator;Password="

' Inizio programma: *********************************************************************************

Set WshShell = WScript.CreateObject("WScript.Shell")
Set FileShell = WScript.CreateObject("Scripting.FileSystemObject")

logTS=Cstr(now) ' memorizzo il TS dell'operazione
getNomeComputer()
InserisciLogs(FileMM)
Wscript.Quit

' Fine Programma ************************************************************************************

sub InserisciLogs(FileName)
    Const ForReading = 1

    on error resume next
    Set TheFile = FileShell.OpenTextFile(FileName, ForReading, False)

    'if Err then
    '   msgbox "Movimento di magazzino non trovato!"
    '   exit sub
    'end if
    
    Do While TheFile.AtEndOfStream <> True
       InserisciLog (TheFile.ReadLine)
    Loop
    TheFile.Close
    set TheFile=FileShell.GetFile(FileName)
    TheFile.Delete ' cancello il file prodotto da CX 
End sub

function InserisciLog(Riga)	
    dim SQLString, MyDB, rsComando
    set MyDB = CreateObject("ADODB.Connection")
    
    MyDB.Open "Driver={SQL Server};Server=server0;Database=gfd;Utente=lognaet;Password=lognaet"
    'MyDB.Open "Driver={SQL Server};Server=server;Database=mic;" + login
	
	'logHN
	'logUserName
	logID_articolo=trim(replace(left(Riga,16),chr(0),""))
	'logID_articolo=replace (logID_articolo," ","")
	logCausale=trim(replace(mid(Riga,17,2),chr(0),""))      '   01 eliminato,     02 Var. Q.,     03 Var. Prezzo,    04 Var. Sconto,     05 Aggiunta
	logTipoDoc=mid(Riga,59,2)
	logSerie=mid(Riga,67,1)
	logNumero=trim(replace(mid(Riga,61,6),chr(0),""))
	logCF=mid(Riga,68,8)
    logPrecedente=replace(mid(Riga,19,20),chr(0),"")  'rtrim(replace(mid(Riga,19,20)," ","*"))  
    logAttuale=replace(mid(Riga,39,20),chr(0),"")
    logData=mid(Riga,80,8)
	logAnno=mid(Riga,76,4)
	'logTS
	logLotto=replace(mid(Riga,12,5),chr(0),"")

	SQLString = "INSERT INTO LogMM (logLotto, logCausale, logHN,logUserName,logDoc ,logSerie ,logCodiceArt, logNumero, logContoCF, logData, logAnno, logTS, logPrecedente, logAttuale) VALUES ('" + logLotto + "','"  + logCausale + "','" + logHN  + "','" + logUserName + "','" + logTipoDoc  + "'," + logSerie+ ",'" + logID_articolo + "'," + logNumero + ",'" + logCF + "','" + logData + "'," + logAnno + ",'" + logTS  + "','" + logPrecedente +  "','" + logAttuale +"');"
	'msgbox SQLString
	
	set rsComando = MyDB.Execute(SQLString) 
	MyDB.Close
end function 

sub getNomeComputer()
	set shell =  Wscript.createobject("Wscript.shell")
	Set WshNetwork = WScript.CreateObject("WScript.Network")

	logUserName= wshNetwork.username 
	logHN= WshNetwork.computername
end sub

