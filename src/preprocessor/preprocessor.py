import abc
import unicodedata

supported_langs = ['en', 'cz']


class PreprocessorConfig:

    def __init__(self, remove_stopwords, to_lowercase=True, remove_accents_before_stemming=False,
                 remove_accents_after_stemming=True):
        self.to_lowercase = to_lowercase
        self.remove_accents_before_stemming = remove_accents_before_stemming
        self.remove_accents_after_stemming = remove_accents_after_stemming
        self.remove_stopwords = remove_stopwords


class Preprocessor:

    def __init__(self, lang, config: PreprocessorConfig, stemmer, tokenizer, stopwords):
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
        if self.config.to_lowercase:
            text = text.lower()

        if self.config.remove_accents_before_stemming:
            text = self.remove_accents(text)

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
            tokens = [self.remove_accents(token) for token in tokens]

        return tokens  # return list of tokens (terms)

    def remove_accents(self, text) -> str:
        """
        Remove accents from a string (Normalization Form KD (NFKD))
        :param text: text to be normalized
        :return:
        """
        ext = text.decode('utf-8')
        return u''.join([c for c in unicodedata.normalize('NFKD', text)
                         if not unicodedata.combining(c)])
