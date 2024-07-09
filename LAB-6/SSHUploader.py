import paramiko
import os

class SSHUploader:
    def __init__(self, hostname, port, username, pkey_path):
        #Connection Params
        self.hostname = hostname
        self.port = port
        self.username = username
        self.pkey_path = pkey_path
        
        #Create SSH client
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try: 
            self.ssh.connect(self.hostname, self.port, self.username, key_filename=self.pkey_path)
            print(f"({hostname}:{port}) Connection to server established!")
        except Exception as e:
            print(f"({hostname}:{port}) Error connecting to server! Error: {e}")

    def upload_file(self, file_path, rfile_path, rfile_name):
        #Create SFTP client
        try:
            self.sftp = self.ssh.open_sftp()
        except Exception as e:
            print(f"({hostname}:{port}) Error creating SFTP session! Error: {e}")

        #Create a folder if it doesn't exist
        try:
            self.sftp.chdir(rfile_path)
        except IOError:
            self.sftp.mkdir(rfile_path)
            self.sftp.chdir(rfile_path)

        print(f"({hostname}:{port}) Changed directory to {rfile_path}")

        #Upload a file
        try:
            self.sftp.put(file_path, rfile_name)
            print(f"({hostname}:{port}) Uploaded {file_path} to {rfile_path}/{rfile_name}")
        except Exception as e:
            print(f"({hostname}:{port}) Error uploading file! Error: {e}")

    def disconnect(self):
        try:
            #Make sure the SFTP Connection is closed
            if self.sftp:
                self.sftp.close()
                print(f"({hostname}:{port}) SFTP session closed successfully!")

            #Close the SSH Connection to the server
            if self.ssh:
                self.ssh.close()
                print(f"({hostname}:{port}) Disconnected from the server.")

        except Exception as e:
            print(f"({hostname}:{port}) Error disconnecting from server! Error: {e}")


if __name__ == '__main__':
    #Connection Params
    hostname = '155.248.219.59'
    port = 22
    username = 'opc'

    #File Params
    pkey_path = 'C:/pkeys/ssh-key-2024-07-04.key'
    file_path = 'Q:/Repos/COMP-216-G3-LABS/LAB-6/transfer-me.txt'
    rfile_path = '/home/opc/transfers'
    rfile_name = 'transfered-text.txt'

    #Create SSHUploader object
    ssh = SSHUploader(hostname, port, username, pkey_path)

    #Connect to the server
    ssh.connect()

    #Upload the file
    ssh.upload_file(file_path, rfile_path, rfile_name)

    #Disconnect from the server
    ssh.disconnect()
    











# #Connection Params
# hostname = '155.248.219.59'
# port = 22
# username = 'opc'

# #File Params
# pkey_path = 'C:/pkeys/ssh-key-2024-07-04.key'
# file_path = 'Q:/Repos/COMP-216-G3-LABS/LAB-6/transfer-me.txt'
# rfile_path = '/home/opc/transfers'
# rfile_name = 'transfered-text.txt'

# #Create SSH client
# ssh = paramiko.SSHClient()
# ssh.load_system_host_keys()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# try:
#     ssh.connect(hostname, port, username, key_filename=pkey_path)
#     print("Connected to the server")

#     sftp = ssh.open_sftp()

#     #Create a folder if it doesn't exist
#     try:
#         sftp.chdir(rfile_path)
#     except IOError:
#         sftp.mkdir(rfile_path)
#         sftp.chdir(rfile_path)

#     print(f"Changed directory to {rfile_path}")

#     #Upload selected file
#     sftp.put(file_path, rfile_name)
#     print(f"Uploaded {file_path} to {rfile_path}/{rfile_name}")

#     # Close SFTP session
#     sftp.close()

# finally:
#     # Close SSH session
#     ssh.close()
#     print("Disconnected from the server")