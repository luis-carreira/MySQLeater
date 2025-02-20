#Necessary modules:

import socket #to get network information

import requests

import json

import os

#custom function library

from lib1 import get_file_paths,create_append_zip, today_for_files

def get_pubip():
    
    """
        Requests public ip adress from the ipinfo API

        it requires requests and json modules

        Adapted from:

    """
    
    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'
        
        exit()

    data = response.json()

    return data['ip']




######################## PROGRAM START ##############################################

############### File Compresion Module ##################################################################

#Compression of all files for SFTP
#1st - Map csv files of the database server backup 

project_path=os.path.dirname(os.path.abspath(__file__))
db_backup_path=project_path+"/db_backup" #path for the database folder

print("Looking up file paths ...")

file_paths2zip=get_file_paths(db_backup_path)

print(file_paths2zip)

print("Compressing files ...")

hostname=socket.gethostname()

# ipv4_addr=socket.gethostbyname(hostname) - will give local host in most cases

ipv4_addr=get_pubip()

dotcounter=0

ipv4_addr_occulted='' #for my eyes only ;)

#in a real scenario ipv4_addr should be used instead

for i in range(0,len(ipv4_addr)):

    if ipv4_addr[i]=='.':

        dotcounter=dotcounter+1

    if dotcounter>=1 and ipv4_addr[i]!='.':

        ipv4_addr_occulted+='x'
    else:

        ipv4_addr_occulted+=ipv4_addr[i]

print(f"Public IP is: {ipv4_addr_occulted}")

zip_name=f"{today_for_files()}_{ipv4_addr_occulted}_{hostname}.zip"

create_append_zip(project_path,zip_name,file_paths2zip)

with open("zip_name.txt",'w') as file:

    file.write(zip_name)











    

