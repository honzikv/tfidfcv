import re


class Tokenizer:
    """
    Default tokenizer
    """

    DEFAULT_REGEX = r'(\d+[.,](\d+)?)|([\p{L}\d]+)|(<.*?>)|([\p{Punct}])'
    URL_REGEX = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][' \
                r'a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,' \
                r'}|www\.[a-zA-Z0-9]+\.[^\s]{2,})/ '
    CENSORED_REGEX = r'\w+\**\w*'
    DATE_REGEX = r'\d{1,2}\.\s?\d{1,2}\.\s*\d{0,4}'

    # Regex used to filter out all non-latin characters - e.g chinese, japanese, etc.
    BASIC_LATIN_CHARACTERS = r'[\p{IsCyrillic}\p{script=Han}\p{script=Hiragana}\p{script=Katakana}\u0600-\u06FF]'

    def __init__(self):
        self.regexes = [Tokenizer.DEFAULT_REGEX, Tokenizer.URL_REGEX, Tokenizer.CENSORED_REGEX, Tokenizer.DATE_REGEX]

    def tokenize(self, text: str):
        """
        Tokenize text
        :param text: text to tokenize
        :return: list of tokens
        """

        # Remove all non-latin characters
        text = re.sub(Tokenizer.BASIC_LATIN_CHARACTERS, '', text)

        # For each regex, find all matches and add them to the set
        tokens = set()
        split_by_ws = text.split(' ')
        for regex in self.regexes:
            regex_tokens = {re.findall(regex, text_by_ws) for text_by_ws in split_by_ws}
            for regex_token in regex_tokens:
                tokens.add(regex_token)  # add each found token to the dictionary

        return tokens
