#!/bin/bash

# Run Python from virtual environment
source /etc/venv/bin/activate
python3 /pathtothefile/url-phishing-report.py

file_not_empty() {
  [[ -s "$1" ]]
}

ip_count=$(cat P_L.txt | wc -l)

if [ $ip_count -gt 0 ]; then
    echo "Please Block these URL"
    cp P_L.txt urls.csv
    cp urls.csv /pathtotheurlphishing/
else
    echo "File P_L.txt has no new URL ."
fi
# cp P_L.txt urls.csv
# cp urls.csv /home/me-ansible/provision/roles/IOCTracker/templates/

if file_not_empty "urls.csv"; then
  echo "urls.csv is not empty, running QradarAPIRefrenceurl.py..."

  # Run IOC_Parser.py to generate ips.csv, hashes.csv, and urls.csv
  #source /etc/venv/bin/activate
  python3 /pathtotheqradarrefrenceaddurl.py/
  python3 /pathtothesplunkurladd.py/
 
else
  echo " urls.csv is empty. Skipping QradarAPIRefrenceurl.py."
fi
