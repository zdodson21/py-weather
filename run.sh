#!/bin/bash

# Text Coloring
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Ensures any commands that display content are displayed on the proper screen
# Check to see if this only should be set when using SSH
export DISPLAY=:0

# Ensures script is being run within Python venv
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Entering Python virtual environment..."
    source .venv/bin/activate
fi

# Fill template and output to weather.html
python jinja.py

# Obtain Screenshot
python screenshot.py

# Display Screenshot
nohup eom -f screenshot.png &
