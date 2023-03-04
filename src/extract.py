import csv
from collections import OrderedDict
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import pandas as pd


def parse_xml(xml_file, output_file):
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


def remove_duplicate_csv(output_file):
    # Open the CSV file and read its contents into a list of dictionaries
    with open(output_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Use OrderedDict to remove duplicate rows based on a specific column
    rows = list(OrderedDict((row['Link'], row) for row in rows).values())

    # Open the CSV file in write mode and write the new rows to it
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def extract_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()


def add_text_website(output_file):
    df = pd.read_csv(output_file)
    df['Text'] = df['Link'].apply(extract_text)
    df.to_csv(output_file, index=False)
