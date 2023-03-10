from src import extract, preprocess, scraping, index, model

def main():
    website = "https://nomanssky.fandom.com/"
    websites_file = "data/websites.json"
    output_file = "data/links.csv"
    db_dir = "data/whoosh"
    child_depth = 1

    print("\n-----------------------\n")
    scraping.check_websites(website, websites_file, child_depth)
    print("\n-----------------------\n")
    extract.json_to_csv(websites_file, output_file)
    print("\n-----------------------\n")
    extract.extract_html_text(output_file)
    print("\n-----------------------\n")
    preprocess.add_preprocessed_text_website(output_file)

    index_db = index.create_database(output_file, db_dir)

    query_text = "What is the release date of No Man\'s sky?"

    documents = index.search_query(query_text, index_db)

    model.answer_question(documents[0]['content'], query_text)


if __name__ == '__main__':
    main()
