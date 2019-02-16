# Zonomi-Bind-Export
A python script for exporting zonomi DNS records to BIND files.
Since zonomi (zonomi.com) does not provide their customers with a way to export BIND 
records for domains, I have created this simple python string to do it. 

# Installation
Requires python 3.x and `requests` library.

# How to Use
Get your zonomi API key from their web dasboard, make a note of your domain name and 
use it as follows:
`export-bind.py ZONOMI-API-KEY domain.name`

A new text file will be created, called domain.name.txt that will contain DNS records
in BIND format.