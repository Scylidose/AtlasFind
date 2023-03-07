import requests  
from bs4 import BeautifulSoup  
from tqdm import tqdm  
import json


# create empty dict
dict_href_links = {}
url = "https://nomanssky.fandom.com/"

def getdata(url):
	r = requests.get(url)
	return r.text


def contain_url_type(url):
	url_types = ["Special:", "Talk:", "Category:",
	             "Help:", "User:", "File:", "No_Mans_Sky_Wiki:",
		         "community.fandom.com"]
	return any([x.lower() in url.lower() for x in url_types])


def get_links(website_link, website):
	html_data = getdata(website_link)
	soup = BeautifulSoup(html_data, "html.parser")
	list_links = []

	for link in soup.find_all("a", href=True):
		# Append to list if new link contains original link
		if str(link["href"]).startswith((str(website_link))) and not contain_url_type(str(link["href"])):
			list_links.append(link["href"])

		# Include all href that do not start with website link but with "/"
		if str(link["href"]).startswith("/") and not contain_url_type(str(link["href"])):
			if link["href"] not in dict_href_links:
				dict_href_links[link["href"]] = None
				link_with_www = website + link["href"][1:]
				link_with_www = link_with_www.split("?")[0]
				list_links.append(link_with_www)

	# Convert list of links to dictionary and define keys as the links and the values as "Unchecked"
	dict_links = dict.fromkeys(list_links, "Unchecked")
	return dict_links

def get_subpage_links(l, website):
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

# Add website WITH slash on end
def check_websites(website, output_file):
    # Create dictionary of website
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

check_websites(url, "data/websites.json")