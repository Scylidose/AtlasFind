import csv
import json
import re
from collections import OrderedDict
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm


def parse_extract_xml(xml_file, output_file):
    """
    Extracts URLs from an XML sitemap file and writes them to a CSV file.

    Args:
        xml_file (str): Path to the XML sitemap file.
        output_file (str): Path to the output CSV file.

    Returns:
        None
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create a new CSV file
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Link'])
        # Loop through each <url> element
        for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            # Extract the link from the <loc> element
            link = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text

            # Write the link to the CSV file
            writer.writerow([link])


def remove_duplicate_csv(output_file, column_name):
    """
    Removes duplicate rows from a CSV file based on a specific column.

    Args:
        output_file (str): Path to the CSV file to remove duplicates from.
        column_name (str): Name of the column to check for duplicates.

    Returns:
        None
    """
    # Open the CSV file and read its contents into a list of dictionaries
    with open(output_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    # Use OrderedDict to remove duplicate rows based on a specific column
    rows = list(OrderedDict((row[column_name], row) for row in rows).values())

    # Open the CSV file in write mode and write the new rows to it
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_html(url):
    """
    Given a URL, retrieves the HTML content of the page, parses it with BeautifulSoup, and returns
    the text of the page as a string.

    Args:
        url (str): A string representing the URL of the page to be parsed.

    Returns:
        str: The text content of the page as a string.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    text = soup.get_text()

    # Remove empty characters and newlines
    text = re.sub('\s+', ' ', text)

    return text


def extract_html_text(output_file):
    """
    Extracts the text from HTML pages linked in a CSV file and saves it in a new column.

    Args:
        output_file (str): the path to the CSV file containing the links

    Returns:
        None
    """
    df = pd.read_csv(output_file)
    print("EXTRACTING HTML\n")
    for i in tqdm(range(len(df))):
        df.loc[i, 'Text'] = parse_html(df.loc[i, 'Link'])
    df.to_csv(output_file, index=False)

    remove_duplicate_csv(output_file, 'Link')


def json_to_csv(json_file, csv_file):
    """
    Reads a JSON file containing links and converts it to a CSV file.

    Args:
        json_file (str): The path to the input JSON file.
        csv_file (str): The path to the output CSV file.

    Returns:
        None
    """
    # Read the JSON file
    with open(json_file) as f:
        data = json.load(f)

    # Extract all the keys
    links = []
    for item in data:
        links.append(item)

    print("TRANSFER JSON TO CSV\n")
    # Write the keys to a new CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Link', 'Text', 'Cleaned'])
        for link in tqdm(links):
            writer.writerow([link, '', ''])