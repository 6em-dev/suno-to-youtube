@echo off
setlocal enabledelayedexpansion

REM Create db directory if it doesn't exist
if not exist "db" mkdir "db"

REM Read the file line by line
for /f "tokens=1,2 delims=|" %%a in (input.txt) do (
    set "filename=%%a"
    set "url=%%b"
    
    REM Use curl to download the file to the db folder
    echo Downloading: !filename!
    curl -o "db\!filename!" "!url!"
    
    REM Wait for 1 second
    timeout /t 1 /nobreak >nul
)