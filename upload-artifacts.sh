#!/bin/bash

env_vars=( "GITHUB_REPOSITORY" "GITHUB_RUN_NUMBER")
missing_vars=()
aws_profile=""

# check if no argument was passed
if [ $# -eq 0 ]; then
  echo "Error: No bucket name argument passed."
  exit 1
fi

if [[ "$2" = "--admin" ]]; then
    aws_profile="--profile admin"
fi

# Check if each environment variable is set
for var in "${env_vars[@]}"
do
    if [[ -z "${!var}" ]]; then
        missing_vars+=($var)
    fi
done

if [ ${#missing_vars[@]} -gt 0 ]; then
    if [ ${#missing_vars[@]} -eq 1 ]; then
      echo "Error: environment variable ${missing_vars[0]} is not set."
    else
      echo "Error: environment variables ${missing_vars[@]} are not set."
    fi
    exit 1
else
    echo "All environment variables are set"
fi

bucket_name=$1
project_name=$GITHUB_REPOSITORY
build_no=$GITHUB_RUN_NUMBER

current_date=$(date +"%Y-%m-%d")

for art in *.zip; do
    [ -f "$art" ] || break # if no files, break
    key=$project_name/$current_date/$build_no/$art
    echo "Info: putting $art to s3 artifact repository $bucket_name with path $key"
    aws s3 cp $art s3://$bucket_name/$key $aws_profile

    if [ $? -ne 0 ]; then
        echo "Error: upload $key failed"
        exit 1
    else
        echo "INFO: upload $key succeeded"
    fi
done

echo "all done"
#TODO: export the keys that were updated so we know what s3 key to pass to the lambda function and lambda layer
