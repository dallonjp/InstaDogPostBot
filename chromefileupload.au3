#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
;**** set path to icon if wanted, not necessary
#AutoIt3Wrapper_Icon=..\..\..\..\Downloads\favicon.ico
#AutoIt3Wrapper_Outfile_x64=chromeupload.exe
#AutoIt3Wrapper_UseX64=y
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
WinWait("[CLASS:#32770]","",10)
ControlFocus("Open","","Edit1")

Sleep(2000)
;**** set path to downloaded photo from api in instadog.py ****
ControlSetText("Open", "", "Edit1", "C:\Users\dallo\instabotdog\00000001.jpg")

Sleep(2000)
ControlClick("Open", "","Button1");