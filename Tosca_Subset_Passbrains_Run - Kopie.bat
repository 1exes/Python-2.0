@echo on


set TOSCAPFAD=C:\Program Files (x86)\TRICENTIS\Tosca Testsuite\ToscaCommander
set WSPACEPFAD=C:\Tosca_Projects\Tosca_Workspaces\Passbrains_V16_P8
set TCSPFAD=C:\Tosca_Projects\ToscaCommander\Keywords
set Dat=%date%_%time:~0,2%-%time:~3,2%-%time:~6,2%

for /F "tokens=1,2,3,4 delims=. " %%a in ('date /t') do set sichdate=%%c_%%b

if not exist "C:\Users\richte\OneDrive - msg systems ag\Tosca\Subsets\"%sichdate% md "C:\Users\richte\OneDrive - msg systems ag\Tosca\Subsets\"%sichdate%

echo starte TC mit ErstelleSubset_Passbrains_Run.tcs

"%TOSCAPFAD%\tcshell.exe" -workspace "%WSPACEPFAD%\Passbrains_V16_P8.tws" -login "EdgarR" "" "%TCSPFAD%\ErstelleSubset_Passbrains_Run.tcs"

move "C:\Tosca_Projects\Subset_Backup\Passbrains_Run.tsu" "C:\Users\richte\OneDrive - msg systems ag\Tosca\Subsets\%sichdate%"

ren "C:\Users\richte\OneDrive - msg systems ag\Tosca\Subsets\%sichdate%\Passbrains_Run.tsu"  "Passbrains_Run_%Dat%.tsu"


