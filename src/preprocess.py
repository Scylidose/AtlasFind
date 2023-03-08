from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string
import nltk
import pandas as pd

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


def remove_duplicates(df, col_name):
    """
    Remove duplicate rows in a specific column of a Pandas DataFrame.
    
    Args:
        df (Pandas DataFrame): The DataFrame to remove duplicates from.
        col_name (str): The name of the column to remove duplicates from.
        
    Returns:
        Pandas DataFrame: The DataFrame with duplicate rows removed.
    """
    # Create a copy of the original DataFrame
    df_copy = df.copy()
    
    # Drop duplicate rows based on the specified column
    df_copy.drop_duplicates(subset=col_name, inplace=True)
    
    return df_copy


def preprocess_text(text):
    """
    Preprocess a text string by converting to lowercase, removing punctuation, 
    removing stopwords, and lemmatizing the remaining words.
    
    Args:
        text (str): The text string to preprocess.
        
    Returns:
        str: The preprocessed text string.
    """
    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove empty characters and newlines
    text = re.sub('\s+', ' ', text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    text_tokens = nltk.word_tokenize(text)
    filtered_text = [word for word in text_tokens if word.lower() not in stop_words]
    text = " ".join(filtered_text)

    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    text_tokens = nltk.word_tokenize(text)
    lemmatized_text = [lemmatizer.lemmatize(word) for word in text_tokens]
    text = " ".join(lemmatized_text)

    return text


def add_preprocessed_text_website(output_file):
    """
    Preprocess the 'Text' column of a CSV file containing website data.
    The preprocessing steps include removing HTML tags, converting to lowercase,
    removing stop words, and lemmatization. Duplicate rows based on the preprocessed text
    are also removed to retain only unique content.
    
    Args:
        output_file (str): The name of the CSV file to preprocess.
        
    Returns:
        None
    """
    df = pd.read_csv(output_file)
    df['Text'] = df['Text'].apply(preprocess_text)
    df = remove_duplicates(df, 'Text')
    df.to_csv(output_file, index=False)
