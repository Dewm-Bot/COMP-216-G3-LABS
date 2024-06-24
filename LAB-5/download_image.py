import requests
import os

#For some dumb reason, not all image links have extensions. We will use this to grab the correct one
def grab_ext(content_type):
	if content_type:
		# Split the content type and get the extension part
		parts = content_type.split('/')
		if len(parts) == 2:
			return '.' + parts[1]
	return ''

def dl_img(url,save_folder):
	try: 
		#Ping Pong. Request the image.
		response = requests.get(url, stream=True)
		response.raise_for_status()

		content_type = response.headers.get('Content-Type')

		#Grab a file extension, just in case.
		ext = grab_ext(content_type)
        
		#grab file name after the "/"
		file_name = url.split('?')[0]
		file_name = file_name.split('/')[-1]
		
		#make sure we actually have an extension for the file. If not, attach it.
		if not file_name.endswith(ext):
			file_name += ext

		#Check if we have a folder name. If not, save in the current directory
		if not save_folder == '':
			#Check if the folder exists. If not, create it.
			if not os.path.exists(save_folder):
				os.makedirs(save_folder)

		
		#Join the folder and file name
		file_name = os.path.join(save_folder, file_name)

		with open(file_name, 'wb') as file:
			#Write the image content to a file
			for chunk in response.iter_content(1024):
				file.write(chunk)
		print(f"Downloaded {file_name}")
	
	except requests.exceptions.RequestException as err:
		print(f"Failed to download file {url}: {err}")

	
if __name__ == "__main__":
	dl_img('https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0', 'single_download')