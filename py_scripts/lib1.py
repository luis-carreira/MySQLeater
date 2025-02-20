import os
import mysql.connector
import csv
from zipfile import ZipFile
import datetime
from cryptography.fernet import Fernet #must have cryptography module installed with pip3
import pyAesCrypt
import subprocess #to run bash commands if needed


def create_folder(folder_path):
    """
    it creates a new folder 

    it requires the os module

    """
    try:
        os.mkdir(folder_path)
        print(f"Folder created with sucess at {folder_path}")
    except FileExistsError:
        print(f"Folder {folder_path} already exists!")
    except Exception as e:
        print(f"Error creating folder: {e}")



def create_mysql_server_connection(host,user,password):
    #estabelish connection with mysql server
    try:

        connection = mysql.connector.connect(
            host=host, #ou servidor remoto
            user=user, 
            passwd=password,    
        )#mudar user conforme necessário user, password 

        print("Connection to server sucessfull!")
        return connection
    
    except OSError as e:
        print(f"Could not connect to the database! Error:{e}")
        return None





def read_query(connection,query):

    """
    
    It excutes a query and makes it possible to retrive its output

    """

    cursor=connection.cursor()

    result=None

    try:
        
        cursor.execute(query)
        result=cursor.fetchall()

        print("Sucess! Closing cursor.")

        cursor.close()

        return result
    
    except mysql.connector.Error as e:

        print(f"Error executing/reading query. Error: {e}")





def run_query(connection, query):

    """
    Executes a query when having a connection with MySQL database

    """

    cursor=connection.cursor()

    result=None

    try: 

        cursor.execute(query)

        connection.commit()

        print(f"Query {query} runned sucessfully")

        cursor.close()

    except mysql.connector.Error as e:

        print(f"Error executing/reading query. Error: {e}")



def create_table_file(connection,tables,folder_path):

    """
    create a csv file for each table with the database
    must already be connected to the server and be using the database

    """

    for table in tables:

        
        db_query=f"DESCRIBE {table};" #to get information for the table

        result=read_query(connection,db_query)

        headers=[header[0] for header in result] #first column of describe gives you the datalabels

        #print(headers) #you can remove this to get less output text

        types=[header[1] for header in result] #second columns gives you the datatypes of each column

        #print(types) #removable also
        
        db_query=f"SELECT * FROM {table};" #new query to get the actual data
        
        rows=read_query(connection,db_query) #all this is the information for the table

        # print(rows) - gives a list of tuples and each tuple is a row

        #you could also:

        # row_list=[]

        # for row in rows:
        
        #row_list=row_list+ [row]

        # print(row_list)

        ##################################################################
        #creation of the file path for the csv file 

        csv_path=folder_path+"/"+table+".csv"

        
        try:
            
            with open(csv_path,'w',newline='') as csvfile:
            
                writer=csv.writer(csvfile)

                writer.writerow(headers) #first row is the data labels for eacg column

                writer.writerow(types) #second row is the data types for each column

                for row in rows: #from the 3rd row it starts the actual data 

                    writer.writerow(row) #adds each row of data to the respective csv file
        except:

            print(f"Error creating {csv_path}!")

        print(f"Table {table} saved sucessfully") #message of sucess for the user





def get_file_paths(main_folder):

    """
    It crawls a directory for sub directories and files

    Adapted from: https://www.geeksforgeeks.org/working-zip-files-python/

    requires os module
    
    """
    
    #list inicitalization to get file paths

    file_paths=[]

    
    try:
        for root, directories, files in os.walk(main_folder):

            for filename in files:

                file_path= os.path.join(root, filename)

                file_paths.append(file_path)

        print(file_paths)     

        return file_paths
    
    except:

        print("Error getting file paths!")
        



def create_append_zip(zip_location,zip_name,file_paths):

    """
        This function creates a new zip and appends files to it 
        The files should be listed as paths in the file_paths list

        requires zipfile module

        import as 

        from zipfile import ZipFile

    """
    try:
        #create zip file path 

        zip_path=f"{zip_location}/{zip_name}"

        #create zip file and add the other files to it

        with ZipFile(zip_path,'w') as zipped:

            for file in file_paths:

                zipped.write(file)

        zipped.close()

        print(f"Files compressed sucessfully at {zip_path}")

    except Exception as e:

        print(f"Error compressing files.\nException: {e}")




def today_for_files():

    """

    it generates a f string with the current data in the format yyyy_mm_dd

    """
    current_time = datetime.datetime.now()

    todayf=f"{current_time.year}_{current_time.month}_{current_time.day}"

    return todayf

def write_key(file_location,name):

    """
    requires the cryptography module install in python3 with  command:

        pip3 install cryptography

    and you must do: 

        from cryptography.fernet import Fernet
    
    it generates a key for AES encription and saves it in a .key file

    """
    key_file=file_location.strip()+'/'+name.strip()+".txt"

    print(f"Full key file path is {key_file}\n")

    key=Fernet.generate_key()

    with open(key_file,"wb") as file:

        file.write(key)
    
    
    #key_file_path=file_location.strip()+'/'+name.strip()+".key"

    
    # to find why this reset step use this: print(key_file)

    return key_file

 
def load_key(key_file):

    return open(key_file,"rb").read()




def encrypt_delete(key,file_path):

    """
        it encrypts a file using the encryption standard AES256-CBC

        requires: import pyAesCrypt

        for more info check the documentation at:
            https://pypi.org/project/pyAesCrypt/

        requires: import os 

    """

    #buffer_size=128*1024 #default buffer size is 64 KB but we need it bigger for the Fernet key

    output_path=f"{file_path}.enc"

    try:
        
        pyAesCrypt.encryptFile(file_path,output_path,key)

        print(f"Encryption sucessful. The output file is: {output_path}")

    except:

        print(f"Error encripting {file_path}")

    
    for i in range(0,3):

        with open(file_path, 'rb+') as f:
            # Overwrite the file content with random bytes of data of the same size
            #this is done 3 times before removal do the file is not easily recovered

            f.write(os.urandom(os.path.getsize(file_path)))


    try:

        os.remove(file_path) #! Deletes the original meaning only the encrypted version remains
        print(f"{file_path} removed sucessfully. However residual data might still remain! ")
        
    except OSError:

        print("Cannot delete a directory!")

    except FileNotFoundError:

        print("File cannot be erased because it does not exit!")

    except:

        print("Unknown error deleting file ")

    
    
    return None




"""
def encrypt(filename,key):

   
    Given a filename (str) and key (bytes), it encrypts the file and re writes it

    Very dangerous - please test first with dummy files
    
   
    f=Fernet(key)

    with open(filename,"rb") as file:

        file_data=file.read()

    encrypted_data=f.encrypt(file_data)

    with open(filename,"wb") as file: 

        file.write(encrypted_data) #overwrites the original file

"""




# def folder_crypt(datadir):

#     file_paths=get_file_paths(datadir)

#     print(file_paths)   

#     for file in file_paths:



def execute_bash_cmd(bash_cmd):

    #sudo commands must be run in root
    
    ls_bash_cmd=bash_cmd.split(" ")

    #print(ls_bash_cmd)
    
    try:
        result=subprocess.run(ls_bash_cmd, capture_output =True, text=True, shell=True)
        print(result)

    except:
        
        print(f"Error running bash command \" {bash_cmd} \"!")

    return None



 