import heapq
from collections import OrderedDict
from typing import List, Dict, Tuple

import numpy as np

from src.document import Document
from src.preprocessing.preprocessor import Preprocessor
from src.tf_idf import DocumentStats


class CosineSimilaritySearch:
    """
    Cosine similarity search implementation
    """

    def __init__(self, tf_idf_inverted_idx: dict, documents: List[Document], preprocessor: Preprocessor):
        """
        Initialize the cosine similarity search
        :param tf_idf_inverted_idx: inverted index containing terms and their stats with documents and tfidf values
        :param documents:
        """
        self.tf_idf_inverted_idx = tf_idf_inverted_idx
        self.documents = documents
        self.total_docs = len(documents)
        self.preprocessor = preprocessor

        # The number of dimensions is equal to the number of terms
        self.dims = len(tf_idf_inverted_idx.keys())
        self.term_to_vec_mapping = OrderedDict({term: idx for idx, term in enumerate(self.tf_idf_inverted_idx)})

    def get_bow_similarity(self, query_bow: dict, document: Document,
                           query_document_stats) -> float:
        """
        Calculates similarity between two bags of words
        :param query_document_stats: dictionary containing terms mapped to document stats of the query
        :param query_bow:
        :param document: document to compare with
        :return: similarity between the two bags of words
        """
        doc_bow = document.bow
        query_vec, doc_vec = np.zeros(self.dims), np.zeros(self.dims)

        # Map values from bow in the query to the vector
        for term, freq in query_bow.items():
            # Get the document stats of the query document for current term and set the tfidf value
            query_vec[self.term_to_vec_mapping[term]] = query_document_stats[term].tfidf

        # Map values from bow in the document to the vector
        for term, freq in doc_bow.items():
            # Get the document stats of this document for current term
            document_stats: DocumentStats = self.tf_idf_inverted_idx[term].documents[document.doc_id]
            doc_vec[self.term_to_vec_mapping[term]] = document_stats.tfidf

        # Finally, calculate the cosine similarity
        return np.dot(query_vec, doc_vec) / (np.linalg.norm(doc_vec) * np.linalg.norm(query_vec))

    def get_query_term_stats(self, query_doc: Document):
        query_bow = query_doc.bow
        term_to_document_stats = {}
        for term, freq in query_bow.items():
            document_stats = DocumentStats(query_doc)
            # for a query document we will use non-log tf since it usually provides better results
            tf = freq
            idf = np.log(self.total_docs / self.tf_idf_inverted_idx[term].df)
            document_stats.set_tfidf(tf * idf)

            term_to_document_stats[term] = document_stats

        return term_to_document_stats

    def get_top_n_documents(self, query: str, n: int) -> List[Tuple[float, Document]]:
        # We need to treat the query as a document
        # Preprocess the query and get the tokens
        query_terms = self.preprocessor.get_processed_tokens(query)

        # Create query document
        query_doc = Document(-1, query_terms)

        # Get bag of words of the query
        query_vec = query_doc.bow

        # Get the cosine similarity of the query with all documents
        results = []

        for doc in self.documents:
            # Get the cosine similarity of the query with the current document
            results.append((np.abs(self.get_bow_similarity(query_vec, doc, self.get_query_term_stats(query_doc))), doc))

        return heapq.nlargest(n, results, key=lambda x: x[0])
