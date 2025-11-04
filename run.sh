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
    echo -e "${RED}Error:${NC} Not running in Python virtual environment"
    echo -e "Please activate virtual environment with: ${BLUE}source .venv/bin/activate${NC} OR ${BLUE}pipenv shell${NC}"
    exit 1
fi

# Fill template and output to weather.html
python jinja.py

# Obtain Screenshot
python screenshot.py

# Display Screenshot
nohup eom -f screenshot.png &

# TODO this is where the timer will be set, and more
# Need to run command so this can run independently as a process
# I must be able to ssh in, start the process, then leave ssh without process stopping.
# I should also be able to ssh in an kill the process or restart it (obviously)
# Look into Chronjon
# I also want it to start by default on start up (set variable or something so this can be disabled) that way
# It accounts for power outages
