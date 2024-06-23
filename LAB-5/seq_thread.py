from download_image import dl_img
import time
import threading

def sequential_download(img_urls):
    start_time = time.perf_counter()
    
    for url in img_urls:
        dl_img(url)
    
    end_time = time.perf_counter()
    
    elapsed_time = end_time - start_time
    print(f"Sequential download completed in {elapsed_time} seconds")

def threaded_download(img_urls):
    start_time = time.perf_counter()
    
    threads = []
    for url in img_urls:
        t = threading.Thread(target=dl_img, args=(url,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end_time = time.perf_counter()
    
    elapsed_time = end_time - start_time
    print(f"Threaded download completed in {elapsed_time} seconds")

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
