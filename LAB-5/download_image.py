import requests

#For some dumb reason, not all image links have extensions. We will use this to grab the correct one
def grab_ext(content_type):
	if content_type:
		# Split the content type and get the extension part
		parts = content_type.split('/')
		if len(parts) == 2:
			return '.' + parts[1]
	return ''

def dl_img(url):
	try: 
		#Ping Pong. Request the image.
		response = requests.get(url, stream=True)
		response.raise_for_status()

		content_type = response.headers.get('Content-Type')

		#Grab a file extension, just in case.
		ext = grab_ext(content_type)
        
		#grab file name after the "/"
		file_name = url.split('/')[-1]
		
		#make sure we actually have an extension for the file. If not, attach it.
		if not file_name.endswith(ext):
			file_name += ext

		with open(file_name, 'wb') as file:
			for chunk in response.iter_content(1024):
				file.write(chunk)
		print(f"Downloaded {file_name}")
	
	except requests.exceptions.RequestException as err:
		print(f"Failed to download file {url}: {err}")

	
dl_img('https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0')