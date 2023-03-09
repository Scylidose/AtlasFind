from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string
import nltk
import pandas as pd
from tqdm import tqdm

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
    punctuation = string.punctuation.replace('-', '')
    text_tokens = nltk.word_tokenize(text)
    text = " ".join([char for char in text_tokens if char not in punctuation])
    # Keep hyphens surrounded by other characters
    text = re.sub(r'[\W\d_](?<![^\W\d_]-(?=[^\W\d_]))', r' ', text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    stop_words.remove("no")
    text_tokens = nltk.word_tokenize(text)
    filtered_text = [word for word in text_tokens if word.lower() not in stop_words]
    text = " ".join(filtered_text)

    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    text_tokens = nltk.word_tokenize(text)
    lemmatized_text = [lemmatizer.lemmatize(word) for word in text_tokens]
    text = " ".join(lemmatized_text)

    # Remove words that contain only one alphabetic character
    text = re.sub(r'\b[a-zA-Z]\b', '', text)

    # Remove empty characters and newlines
    text = re.sub('\s+', ' ', text)

    return text


def remove_common_text(output_file, texts_to_remove):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(output_file)

    for text in texts_to_remove:
        # Remove the value from the column in every row
        df['Cleaned'] = df['Cleaned'].str.replace(text, '')

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

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
    print("PREPROCESSING TEXT\n")
    for i in tqdm(range(len(df))):
        df.loc[i, 'Cleaned'] = preprocess_text(df.loc[i, 'Text'])
    df = remove_duplicates(df, 'Cleaned')
    df.to_csv(output_file, index=False)

    remove_common_text(output_file, ["add category cancel save", "community content available cc by-nc-sa unless otherwise noted advertisement fan feed no man sky wiki starship freighter starbirth explore wikis universal conquest wiki let go luna wiki club wiki explore property fandom muthead futhead fanatical follow overview fandom career press contact term use privacy policy global sitemap local sitemap community community central support help sell info advertise medium kit fandomatic contact fandom apps take favorite fandom never miss beat no man sky wiki fandom game community view mobile site follow ig tiktok join fan lab", "no man sky wiki no man sky wiki explore main page page interactive map navigation main page community portal recent change random page admin noticeboard portal official site community site reddit playstation steam universe galaxy star system planet space station specie resource sentinel technology crafting freighter starship exocraft exosuit multi-tool base building blueprint visual catalogue creativity story mission industrial mining refining cooking tech tree currency additional journal civilized space galactic hub company faction portal lore gamepedia gamepedia support report bad ad help wiki contact fandom home fan central beta game anime movie tv video wikis explore wikis community central start wiki account register sign advertisement no man sky wiki page explore main page page interactive map navigation main page community portal recent change random page admin noticeboard portal official site community site reddit playstation steam universe galaxy star system planet space station specie resource sentinel technology crafting freighter starship exocraft exosuit multi-tool base building blueprint visual catalogue creativity story mission industrial mining refining cooking tech tree currency additional journal civilized space galactic hub company faction portal lore gamepedia gamepedia support report bad ad help wiki contact"])
