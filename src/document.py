class Document:
    """
    Base interface to represent any document that can be indexed
    """

    def __init__(self, doc_id, terms):
        self.doc_id = doc_id
        self.terms = terms
