import os
import streamlit as st
import openai

from src import extract, preprocess, scraping, answer, model, export_doc

def main():
    openai.api_key = os.environ['OPENAI_API_KEY']

    st.title("NMS Data Extraction and Question Answering")

    website = st.text_input("Enter the website URL:", "https://nomanssky.fandom.com/")
    websites_file = "data/websites.json"
    documents_dir = "data/documents"
    output_file = "data/links.csv"
    db_dir = "data/whoosh"
    child_depth = st.slider("Select child depth:", 1, 10, 1)

    if st.button("Start Data Extraction"):
        st.text("Starting data extraction...")
        scraping.check_websites(website, websites_file, child_depth)
        st.text("Data extraction completed.")

    if st.button("Export to CSV"):
        st.text("Exporting data to CSV...")
        extract.json_to_csv(websites_file, output_file)
        st.text("Data exported to CSV.")

    if st.button("Extract HTML Text"):
        st.text("Extracting HTML text...")
        extract.extract_html_text(output_file)
        st.text("HTML text extraction completed.")

    if st.button("Preprocess Text"):
        st.text("Preprocessing text...")
        preprocess.add_preprocessed_text_website(output_file)
        st.text("Text preprocessing completed.")

    query_text = st.text_input("Enter your question:", "What is the release date of No Man's Sky?")
    model_choice = st.selectbox("Select a model:", ["DeepPavlov", "GPT 3.5 - 4k token", "GPT 3.5 - 16k token"])

    if st.button("Answer Question"):
        st.text("Answering the question...")
        if model_choice == "DeepPavlov":
            model_object = model.configure_deeppavlov()
        elif model_choice == "GPT 3.5 - 4k token":
            model_object = "gpt-3.5-4k-tokens" 
            model_choice = "gpt-3.5-4k-tokens"
        elif model_choice == "GPT 3.5 - 16k token":
            model_object = "gpt-3.5-4k-tokens"
            model_choice = "gpt-3.5-16k-tokens"

        answered_question=answer.answer_question(model_choice, model_object, query_text, output_file, db_dir)
        st.text_area("Answer:", answered_question)

if __name__ == '__main__':
    main()