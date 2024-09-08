#!/bin/bash

# Check if the folder name is provided as an argument
if [ $# -eq 0 ]; then
  echo "Please provide at least one folder name as an argument."
  exit 1
fi

FOLDER_NAME=$1

# Create the python folder
mkdir -p python

# Iterate over all provided folder names and copy them to the python folder
for FOLDER_NAME in "$@"
do
  cp -r $FOLDER_NAME python/
done

# Delete any __pycache__ folders
find python/ -name "__pycache__" -exec rm -rf {} +

# Zip the python folder
zip -r ${FOLDER_NAME}.zip python/

# Move the zip file to the lambda_layer folder
mv ${FOLDER_NAME}.zip ../lambda_layer/

# Clean up the python folder
rm -rf python