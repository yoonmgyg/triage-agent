#!/bin/bash
if [ "$ROLE" == "white" ]; then
    python3 greenagent/main_white.py
else
    python3 greenagent/main.py
fi
