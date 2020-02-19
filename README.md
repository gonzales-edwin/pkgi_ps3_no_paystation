# No Pay Station to PKGI PS3 database format script
Python file script to download and convert no pay station file to pkgi ps3 format.
If you've enabled ftp on your PS3, the script will be enabled to upload the filed directly to the PKGI USR folder for you. Just note your IP address before running the script and follow the instructions to run the script with ftp support.

# Run Script

$: pip install -r requirements.txt

## Run without FTP support
$: python file_converter.py

## Run with FTP support

$: python file_converter.py --ftp
