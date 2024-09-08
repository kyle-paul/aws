#!/bin/bash

# Check if at least one model file name is provided as an argument
if [ $# -eq 0 ]; then
  echo "Please provide at least one model file name as an argument."
  exit 1
fi

# Create the python folder
mkdir -p python

# Iterate over all provided model filenames and copy them to the python folder
for MODEL_FILE in "$@"
do
  cp $MODEL_FILE python/
done

# Zip the python folder
zip -r model_layer.zip python/

# Move the zip file to the lambda_layer folder
mv model_layer.zip ../lambda_layer/

# Clean up the python folder
rm -rf python