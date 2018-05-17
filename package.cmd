set folder=douyinMaster

del /F /A /Q build
del /F /A /Q dist
del /F /A /Q __pycache__
del main.spec

if not exist %folder% (
    mkdir %folder%
)

pyinstaller.exe -i logo.ico -F .\main.py
copy dist\main.exe %folder%\douyinMaster.exe
copy tools\* %folder%

"C:\Program Files\7-Zip\7z.exe" a -t7z douyinMaster%date%.7z %folder%\
