from src import extract, preprocess, scraping, answer, model, export_doc

def main():
    website = "https://nomanssky.fandom.com/"
    websites_file = "data/websites.json"
    documents_dir = "data/documents"
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

    query_text = "What is the release date of No Man\'s sky?"
    model_choice = "DeepPavlov"

    if model_choice == "DeepPavlov":
        model_object = model.configure_deeppavlov()
    elif model_choice == "Haystack":
        export_doc.export_documents(output_file, documents_dir)
        model_object = model.configure_haystack(documents_dir)

    answer.answer_question(model_choice, model_object, query_text, output_file, db_dir)


if __name__ == '__main__':
    main()
