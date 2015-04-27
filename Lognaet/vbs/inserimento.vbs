dim WshShell
dim HN, UserName, ComputerName
dim SQLString, MyDB, rsComando
dim OraInizio, OraFine, Righe, DataMexal, TipoInserimento

rem msgbox "Ciao"
Set WshShell = WScript.CreateObject("WScript.Shell")

getNomeComputer()
LogMexal=getLogMexal()
InserisciLog HN, LogMexal, DataMexal, Righe, OraInizio, OraFine, TipoInserimento
Wscript.Quit

function getLogMexal()
    dim tmp

	tmp=""
	Set objArgs = WScript.Arguments

	TipoInserimento=objArgs(0)
	DataMexal=objArgs(1)
	Righe=objArgs(2)
	OraInizio=objArgs(3)
	OraFine=objArgs(4)
	getLogMexal="Data "+ TipoInserimento + ": " + DataMexal + ", dalle " + OraInizio + " alle " + OraFine + ", Righe: " + Righe		
end function

function InserisciLog(Hname, Valore, D, R, Inizio, Fine, Tipo)	
    set MyDB = CreateObject("ADODB.Connection")

	MyDB.Open "Driver={SQL Server};Server=server0;Database=gfd;Utente=lognaet;Password=lognaet"
        'MyDB.Open "Driver= 'dns=mic;'"
	SQLString = "INSERT INTO Logs ( LogHostname, LogUserName, LogDescrizione, logData, logRighe, logOraInizio, logOraFine, logTipo ) VALUES ('" + ComputerName + "','" +UserName +  "','" + Valore +  "','" + D +  "','" + R + "','"  + Inizio +  "','" + Fine +  "','" + Tipo +"');" 
	set rsComando = MyDB.Execute(SQLString) 
	MyDB.Close
end function 

sub getNomeComputer()
	set shell =  Wscript.createobject("Wscript.shell")
	Set WshNetwork = WScript.CreateObject("WScript.Network")

	UserName= wshNetwork.username 
	ComputerName= WshNetwork.computername
end sub

