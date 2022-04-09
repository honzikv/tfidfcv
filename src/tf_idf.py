from typing import List

from src.document import Document
import numpy as np


class DocumentStats:
    """
    Represents stats for specific term in the document
    """

    def __init__(self, document: Document, occurrences: int):
        self.document = document  # Reference to the document
        self.term_count = occurrences  # no. times the term appears in the document
        self._tf = None  # Term frequency
        self._tfidf = None  # Term frequency inverse document frequency

    @property
    def tf(self):
        """
        Returns the term frequency
        This should only be called after the document has been processed
        :return:
        """
        if self._tf is None:
            self._tf = self.term_count / len(self.document.tokens)
        return self._tf

    def set_tfidf(self, tfidf):
        self._tfidf = tfidf

    @property
    def tfidf(self):
        return self._tfidf

    def __str__(self):
        return f"""
        DocumentStats:
            document_id: {self.document.doc_id}
            term_count: {self.term_count}
            term_frequency: {self.tf}
            tfidf: {self.tfidf}"""


class TermStats:
    """
    Represents stats for specific term in the corpus
    """

    def __init__(self, document: Document, term_str: str, occurrences: int):
        self.df = 1  # total number of terms in the corpus
        self.cf = occurrences  # total number of occurrences in the corpus
        self.text = term_str  # mostly for debugging, would not be used in production
        self.documents = {
            document.doc_id: DocumentStats(document, occurrences)
        }  # dictionary containing the documents where the term appears
        self._df = None  # Inverse document frequency

    def add_document_stats(self, document: Document, occurrences: int):
        """
        Updates the document stats for the term
        :param occurrences: number of times the term appears in the document
        :param document: the document
        :return:
        """
        self.cf += occurrences
        self.df += 1
        self.documents[document.doc_id] = DocumentStats(document, occurrences)

    def calculate_tf_idf(self, total_docs: int, log_tf=True):
        """
        Calculates tf-idf weights in each document
        :param: log_tf: if True, tf is calculated as log(1 + tf)
        :return:
        """
        for document in self.documents.values():
            tf = np.log(1 + document.tf) if log_tf else document.tf  # term frequency as an integer
            idf = np.log(total_docs / self.df)
            document.set_tfidf(tf * idf)

    def __str__(self):
        return f"""TermStats:
                collection_frequency: {self.cf}
                document_frequency: {self.df}
                documents: {''.join([str(doc) for doc in self.documents.values()])}"""


def create_inverted_tfidf_idx(documents: List[Document]):
    """
    Creates an inverse index of the documents with calculated tfidf for each term-document pair
    """

    # Create a dictionary of terms and their stats
    inverted_idx = {}
    for document in documents:
        # Get (initialize) bow for the document
        bow = document.bow
        for term, occurrences in bow.items():
            if term not in inverted_idx:
                inverted_idx[term] = TermStats(document, term, occurrences)
            else:
                inverted_idx[term].add_document_stats(document, occurrences)

    # Now that we have the inverted index, we can calculate the tf-idf for each term
    total_docs = len(documents)
    for term in inverted_idx:
        inverted_idx[term].calculate_tf_idf(total_docs)

    return inverted_idx
