#!/bin/bash

# Read the file line by line
while IFS="|" read -r filename url; do
    # Use curl to download the file
    curl -o "$filename" "$url"

    # Wait for 1 second
    sleep 1
done < input.txt
