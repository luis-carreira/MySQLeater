#Necessary modules:

import mysql.connector #for acessing, querying the mysql server and retrieve data
import os #to create folders

#custom function library
from lib1 import create_mysql_server_connection, read_query, run_query
from lib1 import create_table_file, create_folder

######################## PROGRAM START ##############################################

######################### SQL to CSV ####################################

#Disabling system logging and command history
#execute_bash_cmd("service rsyslog stop")
#execute_bash_cmd("HISTSIZE=0")
#execute_bash_cmd("echo $HISTSIZE")

#Get main directories

print("SQL to CSV Module")
print("Fetching data for extrafiltration ...")

project_path=os.path.dirname(os.path.abspath(__file__))
db_backup_path=project_path+"/db_backup" #path for the database folder
print(f"The database will be saved in: {db_backup_path}")
create_folder(db_backup_path) # creates the folder for the csvs with the DB server data

#Creation of a connection object with the database
connection=create_mysql_server_connection("localhost","root","root")

#Finding and listing all the databases
databases=[]

db_query="SHOW DATABASES;"

db_query_result=read_query(connection,db_query)

databases=[i[0] for i in db_query_result]

print(f"The databases of the server are: {databases}")

with open("databases.txt", 'w') as file:

    #saving the databases in a txt file for further use
    
    for database in databases:
        
        file.write(str(database) + "\n")


#Create a folder for each database

for database in databases:

    current_path=db_backup_path+"/"+database

    create_folder(current_path)

    current_path=db_backup_path #reset of the folder path


#Get list of tables and make a folder for each table 
   

for database in databases: #to repeat for each database

    
    current_path=db_backup_path + "/"+database #enter the respective folder of each database 
    
    #SELECT DATABASE 
    
    db_query=f"USE {database};" #select on mysql server the next database
    run_query(connection, db_query) #execute command

    #show tables and get table list
    db_query="SHOW TABLES;" #to get the tables of the database
    
    db_query_result=read_query(connection,db_query)
   
    tables=[table[0] for table in db_query_result] #get the list of the tables

    print(f"For database {database} the tables are: {tables} \n")

    #Make a csv file for each table and fill it with the rows of its respective table

    create_table_file(connection,tables,current_path)


print("Backup sucessfull! Checking database original location...")

#Finding database source directory

db_query="SELECT @@datadir;" #gives you the path where the databases are stored

mysql_datadir=read_query(connection,db_query)

mysql_datadir=mysql_datadir[0] #gets only the first element which is a tuple
mysql_datadir=mysql_datadir[0] #gets a string

with open(f"{db_backup_path}/datadirpath.txt",'w') as file:

    file.write(mysql_datadir)

#Use the following commands to debug and make sure you are getting the correct output
print(mysql_datadir)
print(type(mysql_datadir))

print(f"Data path obtained: {mysql_datadir}")
print("Attempting to close connection to database...")

try:

    connection.close()

    print("MySQL server connection sucessfully closed!")

except:

    print("Error closing MySQL server connection!")






    

