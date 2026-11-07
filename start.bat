@echo off
cd /d "%~dp0"
start "" http://localhost:4200
python serve.py 4200
