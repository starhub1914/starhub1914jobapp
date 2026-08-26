@echo off
echo Starting Software Development Document Environment / My Job App Services...
set PYTHONPATH=.
start /B python python\main.py > python_app.log 2>&1
echo Python 3.14 Engine started in background.
start /B java -cp java\target com.cth.Application > java_app.log 2>&1
echo Java 26 Virtual Threads Engine started in background.
