from typing import List

from src.document import Document


class DocumentStats:
    """
    Represents stats for specific term in the document
    """

    def __init__(self, document: Document):
        self.document = document
        self.term_count = 1

    def increment(self):
        self.term_count += 1


class TermStats:
    """
    Represents stats for specific term in the corpus
    """

    def __init__(self, document: Document):
        self.total_count = 0  # total number of terms in the corpus
        self.documents: {document.doc_id: DocumentStats(document)}  # dictionary of documents where the term appears

    def add_document(self, document: Document):
        self.documents[document.doc_id].increment()


def create_inverse_index(documents: List[Document]):
    """
    Creates an inverse index of the documents.
    """
    inverse_index = {}
    for document in documents:
        tokens = document.tokens
        for token in tokens:
            if token not in inverse_index:
                inverse_index[token] = TermStats(document)


def idx_tf_idf(documents):
