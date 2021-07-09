#!/bin/bash

# TODO: Find latest dataset and download that

# Download zipped dataset
wget https://data.humdata.org/dataset/76f2a2ea-ba50-40f5-b79c-db95d668b843/resource/de2f953e-940c-43bb-b1f8-4d02d28124b5/download/relative-wealth-index-april-2021.zip

# Make destination directory
mkdir rwi_raw_files

# Unzip dataset
unzip relative-wealth-index-april-2021.zip -d rwi_raw_files

# This is the header all input CSV files should have
expected_header="latitude,longitude,rwi,error"

# Write header to all.csv
echo "$expected_header" > all.csv

# For each CSV file in unzipped folder
for filename in rwi_raw_files/*.csv; do
	# Make sure this file has the expected header
	if [[ $(head -n 1 "$filename") == $expected_header ]]; then
		# Append this file, without its header, to all.csv
		cat "$filename" | tail -n +2 >> all.csv
	else
		# There wasn't the expected header. Throw error
		echo "Error: unexpected first line of .csv file. This is either the wrong data, or a newer version!"
		exit 1
	fi
done
