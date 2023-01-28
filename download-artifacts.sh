#!/bin/bash

# Replace <bucket-name> with the actual name of your S3 bucket
bucket_name="gru-deployment-artifacts"

# Get the list of all folders in the S3 bucket
folders=$(aws s3 ls s3://$bucket_name/grug117/waste-schedule-scraper --recursive |  awk '{print $4}')

echo "$folders" | sort -t '/' -k3,3 -k4,4n | echo

# The sort command uses the -t option to specify the delimiter as '/' and the -k option to sort the keys by the 3rd and 4th fields (date and build_num). The -n option sorts the data numerically.
# Then it will get the most recent key by getting the last line of the sorted keys list and then it will use awk to change the format of the key to match the expected format.
sorted_folders=$(echo "$folders" | sort -t '/' -k3,3 -k4,4n)

most_recent_folder=$(echo "$sorted_folders" | awk -F '/' '{print $1"/"$2"/"$3"/"$4"/"}' | uniq | tail -n 1)

aws s3 ls s3://$bucket_name/$most_recent_folder | awk '{print $4}'
aws s3 ls s3://$bucket_name/$most_recent_folder

