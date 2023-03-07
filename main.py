from src import extract, preprocess, scraping 

def main():
    scraping.check_websites("https://nomanssky.fandom.com/", "data/websites.json")

if __name__ == '__main__':
    main()

