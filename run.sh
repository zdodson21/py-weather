#!/bin/bash

# Text Coloring
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Ensures script is being run within Python venv
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${RED}Error:${NC} Not running in Python virtual environment"
    echo -e "Please activate virtual environment with: ${BLUE}source .venv/bin/activate${NC} OR ${BLUE}pipenv shell${NC}"
    exit 1
fi

# TODO this is where the timer will be set, and more
# Need to run command so this can run independently as a process
# I must be able to ssh in, start the process, then leave ssh without process stopping.
# I should also be able to ssh in an kill the process or restart it (obviously)
# Look into Chronjon

