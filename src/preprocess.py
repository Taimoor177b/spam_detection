import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


def preprocess_text(text):

    text = text.lower()

    tokens = word_tokenize(text)

    clean_tokens = []

    for word in tokens:

        if word.isalpha() and word not in stop_words:

            word = lemmatizer.lemmatize(word)

            clean_tokens.append(word)

    return " ".join(clean_tokens)