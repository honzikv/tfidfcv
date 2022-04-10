from src.cosine_similarity import CosineSimilaritySearch
from src.preprocessing.metacritic_preprocessing import deserialize_unpreprocessed_metacritic_reviews, preprocess_reviews
from src.preprocessing.preprocessor import metacritic_preprocessor
from src.tf_idf import create_inverted_tfidf_idx

unpreprocessed_reviews = deserialize_unpreprocessed_metacritic_reviews('resources/unpreprocessed_reviews.json')

# Preprocess the reviews
metacritic_reviews = preprocess_reviews(unpreprocessed_reviews, metacritic_preprocessor)

# Create inverted tfidf index
tf_idf = create_inverted_tfidf_idx(metacritic_reviews)

# Create cosine similarity wrapper object
cos_similarity = CosineSimilaritySearch(tf_idf, metacritic_reviews, metacritic_preprocessor)

# Try some simple queries

# Red Dead Redemption 2
query1 = 'this deserves way higher user score. this game is absolute masterpiece.'

# Cyber shadow
query2 = 'Cyber Shadow is a game that wears its influences on its sleeve and brilliantly weaves together the best elements'

query3 = 'it only looks good, thats all. it can\'t be seemed as real cyberpunk kind game.'

query4 = 'best game ever'

# Search top 10 for each query
for query in [query1, query2, query3, query4]:
    print('Query: ', query)
    print('Top 10 results:')
    results = cos_similarity.get_top_n_documents(query, 10)
    for cos_sim, result in results:
        print(cos_sim, result)
