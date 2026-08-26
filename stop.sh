#!/bin/bash
echo "Stopping Software Development Document Environment / My Job App Services..."
if [ -f .python.pid ]; then
    kill $(cat .python.pid) 2>/dev/null || true
    rm .python.pid
fi
if [ -f .java.pid ]; then
    kill $(cat .java.pid) 2>/dev/null || true
    rm .java.pid
fi
pkill -f "python/main.py" 2>/dev/null || true
pkill -f "com.cth.Application" 2>/dev/null || true
echo "Services stopped cleanly."
