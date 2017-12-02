#!/bin/bash

# Setup script
echo ${BASH_SOURCE}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
venvPython="/home/pi/.virtualenvs/cv/bin/python"
script="opencv.py"

# Echo and run
while true; do
  cmd="\"${venvPython}\" \"${DIR}/${script}\""
  echo $cmd
  eval $cmd
done

