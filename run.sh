#!/bin/bash

# Text Coloring
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Ensures any commands that display content are displayed on the proper screen
# Check to see if this only should be set when using SSH
export DISPLAY=:0

# TODO maybe make it so python virtual environment can be set up automatically, and dependencies can be installed (make sure to include playwright too)

# Ensures script is being run within Python venv
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${RED}Error:${NC} Not running in Python virtual environment"
    echo -e "Please activate virtual environment with: ${BLUE}source .venv/bin/activate${NC} OR ${BLUE}pipenv shell${NC}"
    exit 1
    # TODO make it enter virtual environment for user
fi

# Fill template and output to weather.html
python jinja.py

# Obtain Screenshot
python screenshot.py

# Display Screenshot
nohup eom -f screenshot.png &
