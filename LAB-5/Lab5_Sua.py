
import requests
import time
import threading

def download_image(url):
    try:
        # Send HTTP GET request to download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        file_name = url.split('/')[-1]
        
        # Open a file to write in binary mode and download the content
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f'Downloaded {file_name}')
    
    except requests.exceptions.RequestException as err:
        print(f"Failed to download {url}: {err}")
        
download_image('https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0')

def sequential_download(img_urls):
    start_time = time.perf_counter()
    for url in img_urls:
        download_image(url)
    elapsed_time = time.perf_counter() - start_time
    print(f"Sequential download completed in {elapsed_time:.2f} seconds")


def threaded_download(img_urls):
    start_time = time.perf_counter()
    threads = [threading.Thread(target=download_image, args=(url,)) for url in img_urls]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed_time = time.perf_counter() - start_time
    print(f"Threaded download completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    img_urls = [
        'https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0',
        'https://images.unsplash.com/photo-1485833077593-4278bba3f11f',
        'https://images.unsplash.com/photo-1593179357196-ea11a2e7c119',
        'https://images.unsplash.com/photo-1526515579900-98518e7862cc',
        'https://images.unsplash.com/photo-1582376432754-b63cc6a9b8c3',
        'https://images.unsplash.com/photo-1567608198472-6796ad9466a2',
        'https://images.unsplash.com/photo-1487213802982-74d73802997c',
        'https://images.unsplash.com/photo-1552762578-220c07490ea1',
        'https://images.unsplash.com/photo-1569691105751-88df003de7a4',
        'https://images.unsplash.com/photo-1590691566903-692bf5ca7493',
        'https://images.unsplash.com/photo-1497206365907-f5e630693df0',
        'https://images.unsplash.com/photo-1469765904976-5f3afbf59dfb'
    ]
    
    print("Starting sequential download...")
    sequential_download(img_urls)
    
    print("\nStarting threaded download...")
    threaded_download(img_urls)
