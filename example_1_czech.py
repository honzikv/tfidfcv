import json

from src.doc_id_service import doc_id_service
from src.document import Document
from src.preprocessing.preprocessor import czech_preprocessor
from src.tf_idf import create_inverted_tfidf_idx
from src.cosine_similarity import CosineSimilaritySearch


def get_czech_documents_example():
    # Load documents from json file czech_documents.json
    with open('resources/czech_documents.json', 'r', encoding='utf-8') as f:
        return list(map(lambda x: Document(doc_id_service.get_id(), czech_preprocessor.get_processed_tokens(x['text'])),
                        json.load(f)))


czech_documents = get_czech_documents_example()

# Print the documents
for document in czech_documents:
    print(document)

# Calculate tf-idf for each document

tf_idf = create_inverted_tfidf_idx(czech_documents)

# Print all terms
print(f'Terms: {list(tf_idf.keys())}')

for term, termStats in tf_idf.items():
    print(term, termStats)

# Calculate cosine similarity
query1 = 'Plzeň je krásné město a je to krásné místo'
query2 = 'krásné město'

cosine_similarity = CosineSimilaritySearch(tf_idf, czech_documents, czech_preprocessor)

# top_2_query1 = cosine_similarity.get_top_n_documents(query1, 2)
top_3_query2 = cosine_similarity.get_top_n_documents(query2, 3)

# print('\nQuery 1: ', query1)
# for score, doc in top_2_query1:
#     print(score, '\n', doc)

print('\nQuery 2: ', query2)
for score, doc in top_3_query2:
    print(score, '\n', doc)
