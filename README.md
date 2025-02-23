DISCLAIMER #1: For educational purposes only! Root acess to database and Linux system is required anyway.

DISCLAIMER #2: Not for noobs. Do not use if you are not familiar with SQL databases, Bash, Python and Debian. 

Always test against a virtual environment first!!!
 
This is a set of scripts in Bash and Python3 to simulate a Ransomware attack against a MySQL Server.

The steps performed are the following:
1) A connection to MySQL Server is estabelished (credentials required);
2) The databases are copied to folders and CSV files;
3) The databases are deleted/encrypted;
4) A copy of the folders and CSV files from step 2 are compressed, labeled and sent to a remote server (local address in this case for demo);
5) An encrypted version of the CSV files is left on a folder for the user to find with the decryption script. 
6) Transient files are safely deleted and the ransom message is added and displayed every time a new terminal instance is open.

The scripts are separted by funtionality and maybe be used or edited for other applications, like creating backups or compress and send files
over SSH.

How to use:
1) Change mysql credentials on the sql2csv Python Script.
2) Change SSH/SCP parameters accordingly on the sftp Python Script.
3) Copy/clone the whole directory somewhere on the target machine.
4) Run deploy.sh as root user (not sudo) and wait until it's finished.

I hope you have fun like I did creating this 😄
