import regex as re


class Tokenizer:
    """
    Default tokenizer
    """

    DEFAULT_REGEX = r'(\d+[.,](\d+)?)|([\p{L}\d]+)|(<.*?>)|([\p{Punct}])'
    URL_REGEX = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][' \
                r'a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,' \
                r'}|www\.[a-zA-Z0-9]+\.[^\s]{2,})/ '
    CENSORED_REGEX = r'[\w+À-ž]+\*[\w+À-ž]*|[\w+À-ž]*\*[\w+À-ž]+'
    DATE_REGEX = r'\d{1,2}\.\s?\d{1,2}\.\s*\d{0,4}'

    # Regex used to filter out all non-latin characters - e.g chinese, japanese, etc.
    BASIC_LATIN_CHARACTERS = r'[\p{IsCyrillic}\p{Han}\p{Hiragana}\p{Katakana}\u0600-\u06FF]'

    def __init__(self):
        self.regexes = [Tokenizer.DEFAULT_REGEX, Tokenizer.URL_REGEX, Tokenizer.CENSORED_REGEX, Tokenizer.DATE_REGEX]
        # self.regexes = [Tokenizer.CENSORED_REGEX]

    def tokenize(self, text: str):
        """
        Tokenize text
        :param text: text to tokenize
        :return: list of tokens
        """

        # Remove all non-latin characters
        text = re.sub(Tokenizer.BASIC_LATIN_CHARACTERS, '', text)

        # For each regex, find all matches and add them to the set
        tokens = []
        split_by_ws = text.split(' ')
        for regex in self.regexes:
            for text_by_ws in split_by_ws:
                tokens.extend(self._get_all_regex_items(regex, text_by_ws))

        return tokens

    @staticmethod
    def _get_all_regex_items(regex, text):
        groups = re.findall(regex, text)
        items = []
        for group in groups:
            if type(group) == tuple:
                for item in filter(lambda x: x != '', group):
                    items.append(item)
                continue

            if group != '':
                items.append(group)

        return items
