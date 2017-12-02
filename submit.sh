#!/bin/bash

# Setup script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
script="run.sh"

# New PID so things can run like crazy. Most likely
# there is some process restriction which will kill
# this script eventually (open pipe limit, etc.)
cmd="bash \"${DIR}/${script}\""
echo $cmd
eval $cmd

