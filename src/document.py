class Document:
    """
    Base interface to represent any document that can be indexed
    """

    def __init__(self, doc_id, tokens):
        """
        Initializes the document object
        :param doc_id: the document id
        :param tokens: tokens of the document obtained from preprocessing
        """
        self.doc_id = doc_id
        self.tokens = tokens
        self._bow = None  # bag of words (dictionary of term: frequency in the document)

    def __str__(self):
        return f'Document:\n\tid: {self.doc_id}\n\ttokens: {self.tokens}'

    @property
    def bow(self):
        """
        Returns the bag of words representation of the document
        This property is lazy initialized
        :return:
        """
        if self._bow is None:
            bow = {}
            for token in self.tokens:
                if token not in bow:
                    bow[token] = 1
                else:
                    bow[token] += 1
            self._bow = bow
        return self._bow
