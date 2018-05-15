pyinstaller.exe -i logo.ico -F .\main.py
move dist\main.exe dist\douyinMaster.exe
"C:\Program Files\7-Zip\7z.exe" a -t7z douyinMaster.7z dist\
pause