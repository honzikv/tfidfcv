import logging
import unicodedata
from typing import Iterable

from src.logging import logger_factory
from src.preprocessing.czech_stemmer import CzechStemmer
from src.preprocessing.porter_stemmer import PorterStemmer
from src.preprocessing.tokenizer import Tokenizer
from nltk.stem.porter import PorterStemmer as NLTKPorterStemmer
import langid

logger = logger_factory.get_logger(__name__)

# Recognize all supported languages
langid.set_languages(
    ['af', 'am', 'an', 'ar', 'as', 'az', 'be', 'bg', 'bn', 'br', 'bs', 'ca', 'cs', 'cy', 'da',
     'de', 'dz', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'ga', 'gl', 'gu', 'he', 'hi',
     'hr', 'ht', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'jv', 'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'ky', 'la',
     'lb', 'lo', 'lt', 'lv', 'mg', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'nb', 'ne', 'nl', 'nn', 'no', 'oc',
     'or', 'pa', 'pl', 'ps', 'pt', 'qu', 'ro', 'ru', 'rw', 'se', 'si', 'sk', 'sl', 'sq', 'sr', 'sv', 'sw',
     'ta', 'te', 'th', 'tl', 'tr', 'ug', 'uk', 'ur', 'vi', 'vo', 'wa', 'xh', 'zh', 'zu'])
logger.debug('Langid was configured')


class PreprocessorConfig:

    def __init__(self, lang, remove_stopwords, to_lowercase=True, remove_accents_before_stemming=False,
                 remove_accents_after_stemming=True, remove_punctuation=False):
        self.to_lowercase = to_lowercase
        self.remove_accents_before_stemming = remove_accents_before_stemming
        self.remove_accents_after_stemming = remove_accents_after_stemming
        self.remove_stopwords = remove_stopwords
        self.lang = lang
        self._recognize_lang = False
        self.remove_punctuation = remove_punctuation

    def _get_recognize_lang(self):
        return self._recognize_lang

    def _set_recognize_lang(self, value):
        self._recognize_lang = value
        if value is True:
            logging.info("Language detection is enabled")
        else:
            logging.info("Language detection is disabled")

    recognize_lang = property(_get_recognize_lang, _set_recognize_lang)


class Preprocessor:

    def __init__(self, config: PreprocessorConfig, stemmer, tokenizer: Tokenizer,
                 stopwords: Iterable[str]):
        """
        :param config: config
        :param stemmer: stemmer must have stem() method
        :param tokenizer: tokenizer must have tokenize() method
        """
        self.config = config
        self.stemmer = stemmer
        self.tokenizer = tokenizer
        self.stopwords = stopwords if stopwords else []

    def get_processed_tokens(self, text):
        """
        Get terms from a text and returns them in a list
        :param text: text to be preprocessed
        :return: list of recognized terms occurring in the document
        """

        # First recognize the language via
        if self.config.recognize_lang:
            lang, _ = langid.classify(text)

            # If the language is different raise an exception that must be caught by the caller
            if lang != self.config.lang:
                raise ValueError("Language of the text is not the same as the language of the preprocessor")

        if self.config.to_lowercase:
            text = text.lower()

        if self.config.remove_accents_before_stemming:
            text = self._remove_accents(text)

        # If tokenizer is not passed the text is split by whitespaces
        # Otherwise the tokenize method is called
        tokens = self.tokenizer.tokenize(text, self.config.remove_punctuation) if self.tokenizer else text.split(' ')

        # Remove stop words if toggled
        if self.config.remove_stopwords:
            tokens = [token for token in tokens if token not in self.stopwords]

        # Stem the tokens (skipped if stemmer is not passed)
        if self.stemmer:
            tokens = [self.stemmer.stem(token) for token in tokens]

        # Remove accents after stemming if toggled
        if self.config.remove_accents_after_stemming:
            tokens = [self._remove_accents(token) for token in tokens]

        # logger.info(f'Preprocessed text: {text}')
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
czech_preprocessor = Preprocessor(PreprocessorConfig('cs', remove_stopwords=True), CzechStemmer(), _tokenizer,
                                  _load_czech_stopwords())
english_preprocessor = Preprocessor(PreprocessorConfig('en', remove_stopwords=True), PorterStemmer(), _tokenizer,
                                    _load_english_stopwords())

metacritic_preprocessor = Preprocessor(
    PreprocessorConfig('en', remove_stopwords=True, to_lowercase=True, remove_accents_before_stemming=True,
                       remove_accents_after_stemming=True, remove_punctuation=True), NLTKPorterStemmer(), _tokenizer,
    _load_english_stopwords())
