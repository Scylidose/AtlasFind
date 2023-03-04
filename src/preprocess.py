from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string
import nltk
import pandas as pd

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


def preprocess_text(text):

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
    df = pd.read_csv(output_file)
    df['Text'] = df['Text'].apply(preprocess_text)
    df.to_csv(output_file, index=False)
