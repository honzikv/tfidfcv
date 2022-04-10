from src.cosine_similarity import CosineSimilaritySearch
from src.metacritic_reviews import read_metacritic_reviews
from src.preprocessing.preprocessor import english_preprocessor
from src.tf_idf import create_inverted_tfidf_idx

metacritic_reviews = read_metacritic_reviews('resources/documents.json', english_preprocessor)

tf_idf = create_inverted_tfidf_idx(metacritic_reviews)

cosine_similairty = CosineSimilaritySearch(tf_idf, metacritic_reviews, english_preprocessor)

# RDR2 review
query1 = 'this deserves way higher user score. this game is absolute masterpiece.'

top_10_query = cosine_similairty.get_top_n_documents(query1, 10)

print('\nQuery: ', query1)
for score, doc in top_10_query:
    print(score, '\n', doc)

