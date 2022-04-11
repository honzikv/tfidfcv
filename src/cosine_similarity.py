import ctypes
import heapq
from collections import OrderedDict
from typing import List, Dict, Tuple

import numpy as np

from src.document import Document
from src.preprocessing.preprocessor import Preprocessor
from src.tf_idf import DocumentStats, create_inverted_tfidf_idx


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
        self.term_to_vec_mapping = {term: idx for idx, term in enumerate(self.tf_idf_inverted_idx)}

    @staticmethod
    def append_term_to_vec(terms, term_mapping: Dict[str, int], last_idx):
        for term in terms:
            if term in term_mapping:
                continue
            term_mapping[term] = last_idx[0]
            last_idx[0] = last_idx[0] + 1

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

        # We throw away dimensions where both query and document are zero since they are completely useless
        # and will not change the outcome but boost our performance significantly

        term_mapping = {}
        last_idx = [0]
        self.append_term_to_vec(query_bow.keys(), term_mapping, last_idx)
        self.append_term_to_vec(doc_bow.keys(), term_mapping, last_idx)

        # Create vector for the query and the document
        query_vec = np.zeros(len(term_mapping.keys()))
        doc_vec = np.zeros(len(term_mapping.keys()))
        for term in query_bow.keys():
            query_vec[term_mapping[term]] = query_document_stats[term].tfidf

        for term in doc_bow.keys():
            doc_vec[term_mapping[term]] = self.tf_idf_inverted_idx[term].documents[document.doc_id].tfidf

        # Finally, calculate the cosine similarity
        return np.dot(query_vec, doc_vec) / (np.linalg.norm(doc_vec) * np.linalg.norm(query_vec))

    def get_query_term_stats(self, query_doc: Document):
        query_bow = query_doc.bow
        term_to_document_stats = {}
        for term, freq in query_bow.items():
            document_stats = DocumentStats(query_doc, freq)
            tf = 1 + np.log10(freq)
            idf = np.log10(self.total_docs / self.tf_idf_inverted_idx[term].df)
            document_stats.set_tfidf(tf * idf)

            term_to_document_stats[term] = document_stats

        return term_to_document_stats

    def get_top_n_documents(self, query: str, n: int) -> List[Tuple[float, Document]]:
        # We need to treat the query as a document
        # Preprocess the query and get the tokens
        query_terms = self.preprocessor.get_processed_tokens(query)

        # Filter out those that are not indexed
        # Todo this could be done in a better way
        query_terms = [term for term in query_terms if term in self.tf_idf_inverted_idx]

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


def build_cos_similarity_model(documents: List[Document], preprocessor: Preprocessor):
    """
    Builds a cosine similarity model
    :param documents:
    :param preprocessor:
    :return:
    """
    # Build inverted index
    inverted_idx = create_inverted_tfidf_idx(documents)

    return CosineSimilaritySearch(inverted_idx, documents, preprocessor)
