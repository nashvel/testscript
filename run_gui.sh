#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate the virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Run the GUI
python "$SCRIPT_DIR/git_commit_gui.py"

# Deactivate the virtual environment when done
deactivate
