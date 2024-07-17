import os
import ftplib

class ftpwebmdl:
	def __init__(self,user,password,host,lfolder,rfolder,file_ext='.webm'):
		fail = 0
		self.user = user
		self.password = password
		self.host = host
		self.download_folder = lfolder
		self.file_ext = file_ext
		try:
			self.ftp = ftplib.FTP(host)
			self.ftp.login(user,password)
		except Exception as e:
			print(f"(FAIL) Error connecting to FTP server {host}. Error: {e}")
			fail = 1
		self.folder_name = rfolder
		if fail == 1:
			del self
		else:
			print(f"{self.ftp.host}: Connected to {host} as {user}")
	
	def folderhunt(self, current_dir="/"):
		#Find the folder we want to download from
		found_folders = []
		print(f"{self.ftp.host}: Searching for folder [{self.folder_name}] in {current_dir}")
		try:
			self.ftp.cwd(current_dir)
			items = self.ftp.nlst()
			for item in items:
				item_path = os.path.join(current_dir, item)
				try:
					self.ftp.cwd(item_path)
					if item == self.folder_name:
						found_folders.append(item_path)
						print(f"(SUCCESS) {self.ftp.host}: Found folder {item_path}")
					else:
						found_folders += self.folderhunt(item_path)
				except ftplib.error_perm:
					continue
			self.ftp.cwd("/")
		except Exception as e:
			 print(f"{self.ftp.host}: Error during folder search: {e}")
		return found_folders
	
	def download_webm_files(self,remote_dir):

		#Check if we have a folder name. If not, save in the current directory
		if not self.download_folder == '':
			#Check if the folder exists. If not, create it.
			if not os.path.exists(self.download_folder):
				os.makedirs(self.download_folder)
				print(f"{self.ftp.host}: Folder {self.download_folder} created")
			else:
				print(f"{self.ftp.host}: Folder {self.download_folder} exists")
		print(f"{self.ftp.host}: Downloading files to {self.download_folder}")

		
		#Join the folder and file name
		local_dir = os.path.join(self.download_folder)
		
		#Download webms from found folders
		download_folders = self.folderhunt(remote_dir)
		for folder in download_folders:
			try:
				self.ftp.cwd(folder)
				items = self.ftp.nlst()
				for item in items:
					try:
						if item.endswith(self.file_ext):
							print(f"{self.ftp.host}: Attempting to download {item} from {folder}")
							file_name = os.path.join(local_dir, item)
							with open(file_name, 'wb') as file:
								self.ftp.retrbinary('RETR ' + item, file.write)
							print(f"(SUCCESS) {self.ftp.host}: Downloaded {item} from {folder}")
					except Exception as e:
						print(f"(FAIL) {self.ftp.host}: Error downloading file {item} from {folder}. Error: {e}")
			except Exception as e:
				print(f"(FAIL) {self.ftp.host}: Error downloading files from {folder}. Error: {e}")
		self.ftp.cwd("/")
		print(f"Finished downloading webms from {self.ftp.host}")

	def dl(self,starting_directory):
		if self.ftp:
			try:
				self.download_webm_files(starting_directory)
			except Exception as e:
				print(f"(FAIL) {self.ftp.host}: Error connecting to FTP server. Error: {e}")
			finally:
				self.ftp.quit()
				print(f"Disconnected from {self.ftp.host}")
	
if __name__ == "__main__":
	#Params
	user = "anonymous"
	password = ""
	host = "ftp.gnu.org"
	local_folder = "webm_download"
	remote_folder = "video"
	starting_directory = "/"
	file_ext = ".webm"

	#Init
	try:
		defaultftp = ftpwebmdl(user,password,host,local_folder,remote_folder)
		defaultftp.dl(starting_directory)
	except Exception as e:
		print(f"Error initializing FTP client. Error: {e}")







