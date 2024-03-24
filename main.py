# Import necessary libraries and modules
import hashlib                              # For hashing image content
import io                                   # For handling bytes streams
import pandas as pd                         # For handling CSV files
import requests                             # For making HTTP requests
import os.path                              # For file path operations
import logging                              # For logging errors
from bs4 import BeautifulSoup               # For HTML parsing
from pathlib import Path                    # For handling file paths
from PIL import Image                       # For image processing
from selenium import webdriver              # For web scraping with a headless browser
from selenium.webdriver import EdgeOptions  # For configuring headless browser options

# Configuring logging to write errors to a file
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')


class CSVManager:
    def __init__(self, filename) -> None:
        self.filename = filename

    def __enter__(self):
        # Open CSV file for writing
        self.file = open(self.filename, 'w', encoding="utf-8")
        self.file.write("links\n")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Close CSV file
        self.file.close()

    def save_url_to_csv(self, image_url):
        # Write image URL to CSV file
        self.file.write(image_url + "\n")


def get_content_from_url(url):
    try:
        # Setting up headless browser options
        options = EdgeOptions()
        options.add_argument("--headless=new")
        with webdriver.Edge(options=options) as driver:
            # Accessing URL with a headless browser and getting page content
            driver.get(url)
            page_content = driver.page_source
        return page_content
    except Exception as e:
        # Logging errors when accessing URL
        logging.error(f"Error accessing URL {url}: {e}")
        return None


def parse_image_urls(content):
    try:
        # Parsing image URLs from HTML content using BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")
        for i in soup.findAll('img', attrs={"class":"ts-main-image"}):
            if i:
                image_url = i.get("src")
                if image_url:
                    yield image_url.strip()
    except Exception as e:
        # Logging errors encountered during parsing
        logging.error(f"Error parsing image URLs: {e}")

def parse_and_get_name(content):
    try:
        # Parsing image URLs from HTML content using BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")
        for div in soup.findAll('div', attrs={"class":"headpost"}):
            if div:
                custom_name_element = div.find("h1", attrs={"class": "entry-title"})
                custom_name = custom_name_element.text.strip() if custom_name_element else None
                if custom_name:
                    yield custom_name
    except Exception as e:
        # Logging errors encountered during parsing
        logging.error(f"Error parsing Name: {e}")



def sanitize_filename(filename):
    # Removing forbidden characters from a filename
    forbidden_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', "'", '*']

    for char in forbidden_chars:
        filename = filename.replace(char, " ")

    return filename


def get_and_save_image_to_file(image_url, output_dir, custom_filename=None):
    try:
        # Getting image content from URL and saving it to a file
        image_content = requests.get(image_url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")

        if custom_filename:
            # Generating a custom filename or using a hash of the image content
            sanitized_filename = sanitize_filename(custom_filename)
            filename = sanitized_filename + ".webp"
        else:
            filename = hashlib.sha1(image_content).hexdigest()[:10] + ".webp"
        
        file_path = output_dir / filename
        image.save(file_path, "WebP", quality=95)
    except requests.exceptions.RequestException as e:
        # Logging errors related to requesting image content
        logging.error(f"Request Error saving image {image_url}: {e}")
    except IOError as e:
        # Logging errors related to file IO
        logging.error(f"IOError saving image {image_url}: {e}")
    except Exception as e:
        # Logging general errors encountered during image saving
        logging.error(f"Error saving image {image_url}: {e}")


def get_website_urls(chapters=1):
    # Generating URLs for website pages
    for p in range(1, chapters + 1):
        yield f'https://asuratoon.com/7367709877-myst-might-mayhem-chapter-{p}/'


def main(chapters=1):
    # Main function to execute the scraping and saving process
    with CSVManager("links.csv") as csv_manager:
        for url in get_website_urls(chapters):
            content = get_content_from_url(url)
            if content:
                output_directory = Path(f"./Pictures/{url.split('/')[-2].split('-', 1)[1].replace('-', ' ').title()}")
                output_directory.mkdir(parents=True, exist_ok=True)
                for custom_name in parse_and_get_name(content=content):
                    pass
                for index, image_url in enumerate(parse_image_urls(content=content)):
                    csv_manager.save_url_to_csv(image_url)
                    customized_name = (f"{custom_name} - {index:02}")
                    print(customized_name)
                    get_and_save_image_to_file(
                        image_url, output_dir=output_directory, custom_filename=customized_name)
                    
            else:
                # Logging when empty content is returned for a URL
                logging.warning(f"Empty content returned for URL: {url}")

    print("Done")


if __name__ == "__main__":
    # Running main function with specified parameters and printing 'Done' upon completion
    main(2)
