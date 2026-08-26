#!/bin/bash
echo "Building Software Development Document Environment / My Job App (Linux/macOS)..."
echo "1. Compiling Java 26 Virtual Threads Engine..."
mkdir -p java/target
javac -d java/target java/src/main/java/com/cth/model/JobApplication.java java/src/main/java/com/cth/service/LLMEvaluatorService.java java/src/main/java/com/cth/service/LinkedInBotService.java java/src/main/java/com/cth/Application.java
echo "2. Validating Python 3.14 Async Engine..."
PYTHONPATH=. python3 -m py_compile python/config.py python/models.py python/evaluator.py python/bot.py python/main.py
echo "Build completed successfully."
