Overview:

use this tool to generate sdl and soql files for a provided list of object API names. sdl and soql files will be created with proper conventions to extract and migrate records using an external id field.

Usage:

1) enter your credentials (username, pw+security token) in the documentation/login.xml file
2) set your external ID field on line 23 of run.py
3) modify the desired objects to generate soql and sdl files for in line 22, in a comma separated list
4) execute python run.py
5) voila!

Requirements:

python (version)
packages:
  Beautiful Soup, 
  json, 
  os, 
  requests

