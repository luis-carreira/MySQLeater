
import os #to create folders
import pyAesCrypt #required for decryption - can be obtained from pip


#Place this script where the encrypted files are located along with the file
#containing the decryption key

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
        

def load_key(key_file):

    return open(key_file,"rb").read()


######################## PROGRAM START ##############################################

current_path=os.path.dirname(os.path.abspath(__file__))
key_file="database_encryption_key.txt"

file_paths=get_file_paths(current_path)

key=str(load_key(key_file))

print(key)

#key_corrected=f"b'{key}'"

for file in file_paths:
    
    if file.find(".enc")!=-1:

        #decrypt(key,file)
        
        output_file=file[:-4]
        
        try:
            pyAesCrypt.decryptFile(file,output_file,key)
            print(f"{file} decrypted sucessfully!!!!")
        
        except:
            print(f"Failed to decrypt {file}.\n")

print("If no mistakes were made, all files should now be decrypted! Enjoy :)")