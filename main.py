import os
import requests
from bs4 import BeautifulSoup
import configparser
import zipfile
import shutil
import time
import random
import string

def read_settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')

    url = config.get('Settings', 'url')
    positive_check_text = config.get('Settings', 'positive_check_text')
    negative_check_text = config.get('Settings', 'negative_check_text')
    num_digits = int(config.get('Settings', 'num_digits'))
    zip_filename = config.get('Settings', 'zip_filename')
    allowed_file_types = [ext.strip() for ext in config.get('Settings', 'allowed_file_types').split(',')]
    max_sleep_interval = config.get('Settings', 'max_sleep_interval')
    delete_temp_folder = config.getboolean('Settings', 'delete_temp_folder')  # Updated this line

    return url, positive_check_text, negative_check_text, num_digits, zip_filename, allowed_file_types, max_sleep_interval, delete_temp_folder


def create_default_settings():
    config = configparser.ConfigParser()
    config['Settings'] = {
        'url': 'https://www.peppercarrot.com/0_sources/ep01_Potion-of-Flight/low-res/',
        'positive_check_text': 'en_',
        'negative_check_text': '',
        'num_digits': '3',
        'zip_filename': 'Pepper_and_Carrot',
        'allowed_file_types': 'jpeg, png',
        'max_sleep_interval': '20',
        'delete_temp_folder': 'True'  # Add this line
    }

    with open('settings.ini', 'w') as config_file:
        config.write(config_file)


def is_valid_file_type(file_name, allowed_file_types):
    _, file_extension = os.path.splitext(file_name)
    return file_extension.lower()[1:] in allowed_file_types

def check_existing_files(zip_filename, num_digits):
    # Check if the zip filename already exists in the current directory
    if os.path.isfile(f"{zip_filename}.cbr"):
        print(f"Warning: The zip file '{zip_filename}.cbr' already exists. Exiting the program.")
        return True

    # Check if the individual files specified in settings already exist in the current directory
    for i in range(1, 10**num_digits):
        for ext in ["jpeg", "png"]:
            file_name = f"{i:0{num_digits}d}.{ext}"
            if os.path.isfile(file_name):
                print(f"Warning: The file '{file_name}' already exists. Exiting the program.")
                return True

    return False

def main():
    if not os.path.isfile('settings.ini'):
        print("settings.ini not found. Creating default settings.ini.")
        create_default_settings()

    url, positive_check_text, negative_check_text, num_digits, zip_filename, allowed_file_types, max_sleep_interval, delete_temp_folder = read_settings()

    # Check for existing files before running the program
    if os.path.isfile(f"{zip_filename}.cbr"):
        print(f"Warning: The zip file '{zip_filename}.cbr' already exists. Exiting the program.")
        return

    # Introduce random time interval between requests
    sleep_interval = random.uniform(1, int(max_sleep_interval))
    time.sleep(sleep_interval)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    num_files_to_download = 0
    num_files_skipped = 0
    num_files_downloaded = 0

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        print(f"Saving links with '{positive_check_text}' text and without '{negative_check_text}' text:")

        filtered_links = [link for link in links if positive_check_text in link.text.strip() and negative_check_text not in link.text.strip()]

        # Create a directory with a random name and timestamp
        random_folder_name = f"{time.strftime('%Y%m%d%H%M%S')}_{''.join(random.choice(string.ascii_letters) for _ in range(5))}"
        save_dir = os.path.join(os.getcwd(), random_folder_name)
        os.makedirs(save_dir, exist_ok=True)

        # Loop through the filtered links and save them with numbered file names
        for i, link in enumerate(filtered_links, start=1):
            full_url = url + link['href']
            file_extension = link['href'].split('.')[-1]
            file_name = f"{i:0{num_digits}d}.{file_extension}"

            # Check if the file type is allowed
            if not is_valid_file_type(file_name, allowed_file_types):
                print(f"Warning: Skipping {file_name}. Unsupported file type.")
                num_files_skipped += 1
                continue

            # Check if the file already exists
            if os.path.isfile(file_name):
                print(f"Warning: The file '{file_name}' already exists. Exiting the program.")
                return

            # Save the link content to a file in binary mode
            with open(os.path.join(save_dir, file_name), 'wb') as file:
                file.write(requests.get(full_url, headers=headers).content)

            print(f"Saved: {file_name}")
            num_files_downloaded += 1

        # Zip the files only if there are successfully downloaded files
        if num_files_downloaded > 0:
            zip_file_path = os.path.join(os.getcwd(), f"{zip_filename}.cbr")
            with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                for root, _, files in os.walk(save_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, save_dir))

            print(f"Zipped files into: {zip_file_path}")

        # Delete the temporary folder if it exists and the setting is True
        if delete_temp_folder and os.path.exists(save_dir):
            shutil.rmtree(save_dir)
            print(f"Deleted temporary folder: {save_dir}")
        elif not delete_temp_folder:
            print(f"Warning: Temporary folder '{save_dir}' was not deleted. Please check its contents.")

    else:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")

    # Log at the end of the operation
    print("\nOperation Summary:")
    print(f"Number of files to be downloaded: {len(filtered_links)}")
    print(f"Number of files skipped: {num_files_skipped}")
    print(f"Number of files successfully downloaded: {num_files_downloaded}")

if __name__ == "__main__":
    main()
