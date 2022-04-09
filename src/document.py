class Document:
    """
    Base interface to represent any document that can be indexed
    """

    def __init__(self, doc_id, tokens):
        self.doc_id = doc_id
        self.tokens = tokens
