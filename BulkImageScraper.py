from tkinter import *
import send2trash
import bs4
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox


def download_images():
    query = e1.get()
    directory_name = e2.get()
    url = f'https://unsplash.com/s/photos/{query}'
    parrot = e3.get()


    # Make the file for operations
    os.mkdir(f'/Users/amankumarverma/Desktop/Python/{directory_name}') if (
        not os.path.exists(f'/Users/amankumarverma/Desktop/Python/{directory_name}')) else ""

    # HTML Parsing
    r = requests.get(url)
    htmlcontent = r.content
    soup = bs4.BeautifulSoup(htmlcontent, features='html5lib')

    # Find all the image tags with "src" attributes
    img_tags = soup.find_all('img', src=True)
    list_of_url = []
    # Extract the "src" attributes of the image tags and print them
    for img in img_tags:
        list_of_url.append((img['src']))
    print(list_of_url[0])

    # Download image function
    def download_image(url, folder=f'/Users/amankumarverma/Desktop/Python/{directory_name}/', min_size=50000):
        try:
            response = requests.get(url)
            content_length = response.headers.get('Content-Length')
            if content_length is None or int(content_length) < min_size:
                print(f"Skipping image {url} because it is too small")
                return
            filename = url.split("/")[-1] + '.jpg'
            filepath = os.path.join(folder, filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded successfully at {filepath}")
        except:
            print(f"Error downloading image: {filename}")

    # Bulk downloading using multi-threading
    with ThreadPoolExecutor() as executor:
        for image in list_of_url:
            future = executor.submit(download_image, image)

    # Call ClutterClearingMachine function after all images have been downloaded
    ClutterClearingMachine()

    # Provide feedback to user on GUI when download is completed
    messagebox.showinfo("Download completed!",
                        "All images have been downloaded successfully.")

    # Display a pop-up message if the number of images downloaded is less than the number of images requested by the user

    num_files = len([f for f in os.listdir(f'/Users/amankumarverma/Desktop/Python/{directory_name}') if os.path.isfile(
        os.path.join(f'/Users/amankumarverma/Desktop/Python/{directory_name}', f))])
    messagebox.showwarning("Warning", f" {num_files} images were found for your search query. {num_files} images have been downloaded.")


def ClutterClearingMachine():
    directory_name = e2.get()
    parrot = e3.get()

    PathOfDir = f'/Users/amankumarverma/Desktop/Python/{directory_name}/'
    name = f'{parrot}'

    os.makedirs(
        str(f'/Users/amankumarverma/Desktop/Python/{directory_name}/')) if (not os.path.exists(str(f'/Users/amankumarverma/Desktop/Python/{directory_name}/'))) else ""

    image_number = 1  # Initialize image_number with a value of 1

    for file in (os.listdir(str(f'/Users/amankumarverma/Desktop/Python/{directory_name}/'))):
        filename = os.path.join(
            str(f'/Users/amankumarverma/Desktop/Python/{directory_name}/'), file)
        # print(file)
        if not os.path.isfile(filename):
            continue
        split_tup = os.path.splitext(filename)
        # print(split_tup)
        if file.endswith(""):
            try:
                os.rename(
                    filename, (f"{str(PathOfDir)}/{str(name)} {image_number}{split_tup[-1]}"))
                image_number += 1
            except:
                print("😭 An error occurred with renaming")
        elif file.endswith(split_tup[-1]):
            try:
                os.rename(
                    filename, (f"{str(PathOfDir)}/{str(name)} {image_number}{split_tup[-1]}"))
                image_number += 1
            except Exception as e:
                print(
                    f"An error occurred while renaming the file {filename}: {e}")


def delete_directory():
    directory_name = e2.get()

    if os.path.exists(f'/Users/amankumarverma/Desktop/Python/{directory_name}'):
        send2trash.send2trash(
            f'/Users/amankumarverma/Desktop/Python/{directory_name}')
        print(
            f"The folder at {f'/Users/amankumarverma/Desktop/Python/{directory_name}'} has been moved to the trash/recycling bin.")
        # Provide feedback to user on GUI when delete is completed
        messagebox.showinfo("Delete completed!",
                            "The directory has been deleted successfully.")
    else:
        print(
            f"The folder at {f'/Users/amankumarverma/Desktop/Python/{directory_name}'} does not exist.")


def clear_all():
    # Clear all the input fields
    e1.delete(0, 'end')
    e2.delete(0, 'end')
    e3.delete(0, 'end')



master = Tk()
# Set the title of the GUI window
master.title("Image Downloader")
Label(master, text="What images do you want to download?").grid(row=0)
Label(master, text="Enter the file in which you want to do the operations:").grid(row=1)
Label(master, text="Enter the name of the images to be saved as:").grid(row=2)


e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)


e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)


# Add a new Button widget for the "Clear All" button
Button(master, text='Clear All Inputs', command=clear_all).grid(
    row=7, column=1, sticky=W, pady=4)
Button(master, text='Download Images', command=download_images).grid(
    row=4, column=1, sticky=W, pady=4)
Button(master, text='Delete Folder', command=delete_directory).grid(
    row=6, column=1, sticky=W, pady=4)
mainloop()
