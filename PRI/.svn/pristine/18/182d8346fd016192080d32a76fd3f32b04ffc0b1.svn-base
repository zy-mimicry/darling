@set port=8080
@cd "%~dp0"
@set waitingtile=PRI_System web server(Django) waiting on %port% %cd%
@set runningtile=PRI_System web server(Django) running on %port% %cd%
@title %waitingtile%
@hostname>%tmp%\hostname.txt
@set /p hostname=<%tmp%\hostname.txt
@rem echo hostname=%hostname%
@set "winrar=C:\Program Files (x86)\WinRAR\WinRAR.exe"
@if not exist "%winrar%" @set "winrar=C:\Program Files\WinRAR\WinRAR.exe"
@if not exist "templates\LigerUI\lib" @(
    call "%winrar%" x jQuery+LigerUI+V1.3.3.rar Source\* templates\ -y
    robocopy /e /np /ndl /nfl templates\Source templates\LigerUI
    rd /s /q templates\Source
)
@if not "%~1"=="" @(
    @taskkill /f /t /fi "windowtitle eq %runningtile%"
    @echo delay %~1 senconds here ...
    @ping 1.2.3.4 -w 1000 -n %~1 >nul 2>&1
)
@taskkill /f /t /fi "windowtitle eq %runningtile%"
@title %runningtile%
@if not "%~1"=="" @(
    @echo delay %~1 senconds here ...
    @ping 1.2.3.4 -w 1000 -n 10 >nul 2>&1
)
@set scheduler=False
@python manage.py runserver %hostname%:%port%