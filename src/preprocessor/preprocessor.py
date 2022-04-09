import os
import unicodedata
from typing import Iterable

from src.preprocessor.czech_stemmer import CzechStemmer
from src.preprocessor.porter_stemmer import PorterStemmer
from src.preprocessor.tokenizer import Tokenizer


class PreprocessorConfig:

    def __init__(self, remove_stopwords, to_lowercase=True, remove_accents_before_stemming=False,
                 remove_accents_after_stemming=True):
        self.to_lowercase = to_lowercase
        self.remove_accents_before_stemming = remove_accents_before_stemming
        self.remove_accents_after_stemming = remove_accents_after_stemming
        self.remove_stopwords = remove_stopwords


class Preprocessor:

    def __init__(self, lang, config: PreprocessorConfig, stemmer, tokenizer: Tokenizer,
                 stopwords: Iterable[str]):
        """
        :param lang: language of the text
        :param config: config
        :param stemmer: stemmer must have stem() method
        :param tokenizer: tokenizer must have tokenize() method
        """
        self.lang = lang
        self.config = config
        self.stemmer = stemmer
        self.tokenizer = tokenizer
        self.stopwords = stopwords if stopwords else []

    def get_terms(self, text):
        """
        Get terms from a text and returns them in a list
        :param text: text to be preprocessed
        :return: list of recognized terms occurring in the document
        """
        if self.config.to_lowercase:
            text = text.lower()

        if self.config.remove_accents_before_stemming:
            text = self._remove_accents(text)

        # If tokenizer is not passed the text is split by whitespaces
        # Otherwise its tokenize() method is called
        tokens = self.tokenizer.tokenize(text) if self.tokenizer else text.split(' ')

        # Remove stop words if toggled
        if self.config.remove_stopwords:
            tokens = [token for token in tokens if token not in self.stopwords]

        # Stem the tokens (skipped if stemmer is not passed)
        if self.stemmer:
            tokens = [self.stemmer.stem(token) for token in tokens]

        # Remove accents after stemming if toggled
        if self.config.remove_accents_after_stemming:
            tokens = [self._remove_accents(token) for token in tokens]

        return tokens  # return list of tokens (terms)

    @staticmethod
    def _remove_accents(text) -> str:
        """
        Remove accents from a string (Normalization Form KD (NFKD))
        :param text: text to be normalized
        :return:
        """
        # text = text.decode('utf-8')
        return u''.join([c for c in unicodedata.normalize('NFKD', text)
                         if not unicodedata.combining(c)])


def _load_czech_stopwords():
    """
    Loads Czech stop words from file.
    """
    with open('resources/czechST.txt', 'r', encoding='utf-8') as file:
        return file.read().split('\n')


def _load_english_stopwords():
    """
    Loads English stop words from file.
    """
    with open('resources/englishST.txt', 'r', encoding='utf-8') as file:
        return file.read().split('\n')


_tokenizer = Tokenizer()

# Default instances
czech_preprocessor = Preprocessor('cs', PreprocessorConfig(remove_stopwords=True), CzechStemmer(), _tokenizer,
                                  _load_czech_stopwords())
english_preprocessor = Preprocessor('en', PreprocessorConfig(remove_stopwords=True), PorterStemmer(), _tokenizer,
                                    _load_english_stopwords())
