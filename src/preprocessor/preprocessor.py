supported_langs = ['en', 'cz']


class Preprocessor:

    def __init__(self, lang='en'):
        if lang not in supported_langs:
            raise ValueError('Language not supported')

        self.lang = lang
        
