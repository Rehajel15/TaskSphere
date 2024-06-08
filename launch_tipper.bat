@ECHO off

call ./.venv/Scripts/activate.bat

start "" /b python manage.py runserver

start "" /b npm run TaskSphere
