import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data (only if not already downloaded)
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download('punkt_tab')

stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

def nltk_tokenizer(text: str) -> list[str]:
    """
    Tokenize + lowercase + stem + remove stopwords/punct
    
    Breaks a sentence into clean, searchable keywords.
    Steps:
    1. Lowercase everything → "Tea" -> "tea"
    2. Split sentence into words
    3. Remove punctuation + common boring words ("the", "and", "is", ...)
    4. Reduce words to their root form → "making" -> "make"

    Example:
        "How to make tea?" → ["make", "tea"]

    """

    words = word_tokenize(text.lower())
    tokens = [
        stemmer.stem(w)
        for w in words if w.isalnum() and w not in stop_words
    ]

    return tokens
