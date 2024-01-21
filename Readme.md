# Comic Book Downloader and CBR Creator

This Python script, named `main.py`, allows users to download their favorite comics available online from a folder for portable usage. It utilizes BeautifulSoup for web scraping and Requests for HTTP requests. Please read the following information and adhere to the license and fair use policy.

## Fair Use Warning

The code allows users to download their favorite comics available online for portable usage. However, several authors do not permit downloading and storing of the artwork. The user is obligated to follow the license policy of the original artist and only use this script under the fair use policy. Any abuse or piracy for commercial purposes is the sole responsibility of the user. The code author shall not be responsible for illegal activities.

## License

This script is licensed under the [Commons Clause](https://commonsclause.com/) License Condition v1.0 - see the [LICENSE.md](LICENSE.md) file for details.

**Important Note**: This license strictly prohibits any commercial redistribution of the script. Users are encouraged to read and understand the terms specified in the [LICENSE.md](LICENSE.md) file.

## Acknowledgment

The sample comic "Pepper and Carrot" used in this script is taken from [Pepper and Carrot](https://www.peppercarrot.com/), a free(libre) and open-source webcomic supported directly by its patrons. You can support the author, [David Revoy](https://www.davidrevoy.com/), directly on his [Patreon page](https://www.patreon.com/join/davidrevoy).



## Settings.ini Variables

- **url**: The URL of the website to scrape.
- **positive_check_text**: Text to check for in the links to be included.
- **negative_check_text**: Text to check for exclusion in the links (optional).
- **num_digits**: Number of digits to use for numbering files.
- **zip_filename**: Name of the zip file to be created.
- **allowed_file_types**: Comma-separated list of allowed file types (e.g., jpeg, png).
- **max_sleep_interval**: Maximum random time interval (in seconds) between requests.
- **delete_temp_folder**: Boolean value (True/False) to determine whether to delete the temporary folder after operation.

## How to Generate Default Settings

If the `settings.ini` file is not available, the script will automatically generate default settings when run for the first time. The default settings are as follows:

```ini
[Settings]
url = https://www.peppercarrot.com/0_sources/ep01_Potion-of-Flight/low-res/
positive_check_text = en_
negative_check_text = 
num_digits = 3
zip_filename = Pepper_and_Carrot
allowed_file_types = jpeg, png
max_sleep_interval = 20
delete_temp_folder = True
```

You can customize these settings by editing the settings.ini file manually.

## Installing Dependencies

Before running the script, ensure you have the required dependencies installed. You can install them using the following command:
```bash
pip install -r requirements.txt
```


## Running the Script

To run the script:

1. Ensure Python is installed on your system.
2. Install required packages by running: pip install -r requirements.txt.
3. Run the script: python main.py.

The script will download files based on the specified settings and provide an operation summary at the end.

