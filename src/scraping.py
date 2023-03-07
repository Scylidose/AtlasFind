import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json


# create empty dict
dict_href_links = {}


def getdata(url):
	"""
	Retrieves the HTML content of the specified URL.

	Args:
		url (str): The URL to retrieve the data from.

	Returns:
		str: The HTML content of the specified URL.
	"""
	r = requests.get(url)
	return r.text


def contain_url_type(url):
	"""
	Checks if the given URL contains any of the specified URL types.

	Args:
		url (str): The URL to check.

	Returns:
		bool: True if the URL contains any of the specified URL types, False otherwise.
	"""
	url_types = ["Special:", "Talk:", "Category:",
				 "Help:", "User:", "File:", "No_Mans_Sky_Wiki:",
				 "community.fandom.com"]
	return any([x.lower() in url.lower() for x in url_types])


def get_links(website_link, website):
	"""
	Retrieves all links from a given website URL and returns them as a dictionary.

    Args:
        website_link (str): The URL of the website to retrieve links from.
        website (str): The base URL of the website.

    Returns:
        dict: A dictionary containing all links from the website as keys, with
			 "Unchecked" as the default value.
    """
	html_data = getdata(website_link)
	list_links = []
	
	soup = BeautifulSoup(html_data, "html.parser")

	for link in soup.find_all("a", href=True):
		# Append to list if new link contains original link
		if str(link["href"]).startswith((str(website_link))) and not contain_url_type(str(link["href"])):
			list_links.append(link["href"])

		# Include all href that do not start with website link but with "/"
		if str(link["href"]).startswith("/") and not contain_url_type(str(link["href"])) and not "/nomanssky.fandom.com" in str(link["href"]):
			if link["href"] not in dict_href_links:
				dict_href_links[link["href"]] = None
				link_with_www = website + link["href"][1:]
				link_with_www = link_with_www.split("?")[0]
				link_with_www = link_with_www.split("#")[0]

				list_links.append(link_with_www)

	# Convert list of links to dictionary and define keys as the links and the values as "Unchecked"
	dict_links = dict.fromkeys(list_links, "Unchecked")
	return dict_links

def get_subpage_links(l, website):
	"""
	Crawls all unchecked links in a given dictionary of links and
	adds any new links found to the same dictionary.

    Args:
        l (dict): A dictionary containing links to crawl, with the
				  status of each link as the value.
        website (str): The base URL of the website.

    Returns:
        dict: A dictionary containing all crawled links as keys,
			  with their status as the value.
    """
	for link in tqdm(l):
		# If not crawled through this page start crawling and get links
		if l[link] == "Unchecked":
			dict_links_subpages = get_links(link, website)
			# Change the dictionary value of the link to "Checked"
			l[link] = "Checked"
		else:
			# Create an empty dictionary in case every link is checked
			dict_links_subpages = {}
		# Add new dictionary to old dictionary
		l = {**dict_links_subpages, **l}
	return l

def check_websites(website, output_file):
	"""
	Crawls all pages on a website, saves the links to a dictionary, and
	writes the dictionary to a JSON file.

    Args:
        website (str): The base URL of the website to crawl.
        output_file (str): The name of the output JSON file to write the
						   dictionary of links to.

    Returns:
        None
    """
	# Create dictionary of website
	# Add website WITH slash on end
	dict_links = {website:"Unchecked"}

	counter, counter2 = None, 0
	while counter != 0:
		counter2 += 1
		dict_links2 = get_subpage_links(dict_links, website)
		
		counter = sum(value == "Unchecked" for value in dict_links2.values())
		dict_links = dict_links2

		# Save list in json file
		a_file = open(output_file, "w", encoding='utf-8')
		json.dump(dict_links, a_file)
		a_file.close()
