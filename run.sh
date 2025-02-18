#!/usr/bin/env bash

# Check if virtual environment exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    python main.py "$@"
    deactivate
    exit 0
fi

# Check if conda is available
if command -v conda &> /dev/null; then
    if conda env list | grep -q "xc-cup-env"; then
        conda run -n xc-cup-env python main.py "$@"
        exit 0
    fi
fi

# Fallback to system python
python3 main.py "$@"

