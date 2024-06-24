from download_image import dl_img
from seq_thread import threaded_download, sequential_download


def menu():
    #single download URL
    test_url = "https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0"
    #multi download URLs
    test_url_list = [
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


    #prompt user for what they want to do
    while True:
        print("\nSelect an option:")
        print("1. Download a test image")
        print("2. Sequential download test")
        print("3. Threaded download test")
        print("4. Sequential and Threaded download speed test")
        print("5. Download specified image from URL")
        print("6. Download images from URLs")
        print("0. Exit \n\n")
        #get user input
        choice = input("Enter your choice: ")


        if choice == '1':  
        #Single download
            print("\n\n")
            single_folder = 'single-download'
            dl_img(test_url, single_folder)
        elif choice == '2':
        #Sequential download
            print("\n\n")
            seq_folder = "sequential-downloads"
            sequential_download(test_url_list, seq_folder)
        elif choice == '3':
        #Threaded download
            print("\n\n")
            thread_folder = "threaded-downloads"
            threaded_download(test_url_list, thread_folder)
        elif choice == '4':
        #Speed test
            print("\n\n")
            seqrace_folder = "seq-race-downloads"
            threadrace_folder = "thread-race-downloads"
            sequential_download(test_url_list, seqrace_folder)
            threaded_download(test_url_list, threadrace_folder)
        elif choice == '5':
        #Download image from URL
            print("\n\n")
            url = input("Enter the URL of the image: ")
            folder = input("Enter folder name: ")
            try:
                dl_img(url, folder)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '6':
        #Download images from URLs
            print("\n\n")
            url_list = []
            print("Enter image URLs (type 'end' to finish):")
            while True:
                url = input()
                if url.lower() == 'end': #check if the user wants to stop entering URLs
                    break
                url_list.append(url) #add the URL to the list
            folder = input("Enter the folder to save the images: ")
            method = input("Type 's' for sequential download or 't' for threaded download: ")
            if method.lower() == 's':
                try:
                    sequential_download(url_list, folder)
                except Exception as e:
                    print(f"Error: {e}")
            elif method.lower() == 't':
                try:
                    threaded_download(url_list, folder)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Invalid choice: Please select Threaded or Sequential download")
        elif choice == '0':
            print("Exiting.")
            break
        else:
            print("Invalid choice: Please try again.")

if __name__ == "__main__":
    menu()

