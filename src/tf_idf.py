from typing import List

from src.document import Document
import numpy as np


class DocumentStats:
    """
    Represents stats for specific term in the document
    """

    def __init__(self, document: Document):
        self.document = document  # Reference to the document
        self.term_count = 1  # no. times the term appears in the document
        self._tf = None  # Term frequency
        self._tfidf = None  # Term frequency inverse document frequency

    def increment(self):
        """
        Increments the term count by one
        :return:
        """
        self.term_count += 1

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


class TermStats:
    """
    Represents stats for specific term in the corpus
    """

    def __init__(self, document: Document):
        self.total_count = 0  # total number of terms in the corpus
        self.documents = {
            document.doc_id: DocumentStats(document)
        }  # dictionary containing the documents where the term appears
        self._df = None  # Inverse document frequency

    def update_document_stats(self, document: Document):
        """
        Updates the document stats for the term
        :param document:
        :return:
        """
        self.documents[document.doc_id].increment()

    @property
    def df(self):
        """
        Returns the document frequency of the term
        :return:
        """
        if self._df is None:
            self._df = len(self.documents) / self.total_count
        return self._df

    def calculate_tf_idf(self, total_docs: int, log_tf=True):
        """
        Calculates tf-idf weights in each document
        :param: log_tf: if True, tf is calculated as log(1 + tf)
        :return:
        """
        for document in self.documents.values():
            tf = 1 + np.log(document.tf) if log_tf else document.tf  # term frequency as an integer
            df = self.df
            document.set_tfidf(tf * np.log(total_docs / df))


def create_inverted_tfidf_idx(documents: List[Document]):
    """
    Creates an inverse index of the documents with calculated tfidf for each term-document pair
    """

    # Create a dictionary of terms and their stats
    inverted_idx = {}
    for document in documents:
        tokens = document.tokens
        for token in tokens:
            if token not in inverted_idx:
                inverted_idx[token] = TermStats(document)
            else:
                inverted_idx[token].update_document_stats(document)

    # Now that we have the inverted index, we can calculate the tf-idf for each term
    total_docs = len(documents)
    for term in inverted_idx:
        inverted_idx[term].calculate_tf_idf(total_docs)

