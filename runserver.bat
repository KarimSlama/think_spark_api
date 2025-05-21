@echo off
cd /d "E:\Django Projects\think-spark"
call Scripts\activate.bat
cd src
set DJANGO_SETTINGS_MODULE=project.settings
set PYTHONPATH=.
python -m daphne -b 192.168.1.7 -p 8000 project.asgi:application
pause
