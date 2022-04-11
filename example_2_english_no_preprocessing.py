import json

from src.doc_id_service import doc_id_service
from src.document import Document
from src.preprocessing.whitespace_preprocessor import SplitPreprocessor
from src.tf_idf import create_inverted_tfidf_idx
from src.cosine_similarity import CosineSimilaritySearch


def get_english_documents_example():
    # Load documents from json file czech_documents.json
    with open('resources/english_documents.json', 'r', encoding='utf-8') as f:
        return list(map(lambda x: Document(doc_id_service.get_id(), x['text'].split(' ')),
                        json.load(f)))


english_documents = get_english_documents_example()

# Print the documents
for document in english_documents:
    print(document)

# Calculate tf-idf for each document
tf_idf = create_inverted_tfidf_idx(english_documents)

# Print all terms
print(f'Terms: {list(tf_idf.keys())}')

for term, termStats in tf_idf.items():
    print(term, termStats)

# Calculate cosine similarity
query1 = 'tropical fish sea'
query2 = 'tropical fish'

cosine_similarity = CosineSimilaritySearch(tf_idf, english_documents, SplitPreprocessor())

q1 = cosine_similarity.get_top_n_documents(query1, 5)
q2 = cosine_similarity.get_top_n_documents(query2, 5)

print('\nQuery 1: ', query1)
for score, doc in q1:
    print(score, '\n', doc)

print('\nQuery 2: ', query2)
for score, doc in q2:
    print(score, '\n', doc)
