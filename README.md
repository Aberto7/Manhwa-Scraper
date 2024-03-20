# Manhwa-Scraper

Manhwa Scraper is a Python script designed to scrape Manhwa chapters from a website and save the images locally. It also logs any errors encountered during the process.

## What the Code Does

The script performs the following tasks:

1. Accesses specified URLs using a headless browser.
2. Parses the HTML content of the pages to extract image URLs.
3. Downloads the images and saves them locally in a specified directory.
4. Writes the image URLs to a CSV file.
5. Logs any errors encountered during the process to a file.

## Installation and Configuration

To run this script, you need to have Python installed on your system. Additionally, you need to install the following Python libraries and modules:

- `hashlib`
- `io`
- `pandas`
- `requests`
- `os.path`
- `logging`
- `bs4` (BeautifulSoup)
- `pathlib`
- `PIL` (Pillow)
- `selenium`

You can install these libraries using pip:

```bash
pip install pandas requests beautifulsoup4 pillow selenium
```

You also need to have the Edge WebDriver installed on your system for Selenium to work. You can download it from the [Microsoft Edge Developer site](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).

Once you have everything installed, you can run the script using Python:

```bash
python manhwa_scraper.py
```

By default, the script will scrape the first 10 chapters of the Manhwa. You can change this by modifying the argument passed to the `main` function in the `if __name__ == "__main__":` block.

The images will be saved in a directory named "Pictures" in the same directory as the script. Each chapter will have its own subdirectory. The image URLs will be saved in a file named "links.csv".

Please note that the script is currently configured to scrape from 'https://asuratoon.com/'. If you want to scrape from a different website, you will need to modify the `get_website_urls` function and possibly the `parse_image_urls` function to correctly extract the image URLs. 

## Error Logging

The script logs any errors encountered during the process to a file named 'error.log'. This includes errors when accessing URLs, parsing content, and saving images. If the script is not working as expected, you can check this file for any error messages. 

## Disclaimer

Please use this script responsibly and respect the terms of use of the website you are scraping from. Web scraping may be against the terms of service of some websites, and the data you scrape should not be used for commercial purposes without permission.