#!/bin/bash
echo "Starting Software Development Document Environment / My Job App Services..."
export PYTHONPATH=.
python3 python/main.py > python_app.log 2>&1 &
PYTHON_PID=$!
echo $PYTHON_PID > .python.pid
echo "Python 3.14 Engine started with PID $PYTHON_PID"

java -cp java/target com.cth.Application > java_app.log 2>&1 &
JAVA_PID=$!
echo $JAVA_PID > .java.pid
echo "Java 26 Virtual Threads Engine started with PID $JAVA_PID"
echo "Application startup initiated."
