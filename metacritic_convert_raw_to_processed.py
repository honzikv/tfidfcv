import logging

from src.logging import logger_factory
from src.preprocessing.metacritic_preprocessing import load_metacritic_reviews, preprocess_reviews, \
    serialize_preprocessed_reviews, serialize_unpreprocessed_metacritic_reviews
from src.preprocessing.preprocessor import metacritic_preprocessor

# Script to convert rawdata.json to processed data

logger = logger_factory.get_logger(__name__)

logger.info('Loading metacritic reviews')
raw_file_path = 'resources/rawdata.json'
metacritic_reviews = load_metacritic_reviews(raw_file_path)

# Save mapped reviews to file
logger.info('Saving unpreprocessed metacritic reviews')
unpreprocessed_file_path = 'resources/unpreprocessed_reviews.json'
serialize_unpreprocessed_metacritic_reviews(metacritic_reviews, unpreprocessed_file_path)


logger.info('Preprocessing metacritic reviews')
# Preprocess them
metacritic_preprocessor.config.recognize_lang = True  # enable language recognition
preprocessed_reviews = preprocess_reviews(metacritic_reviews, metacritic_preprocessor)

logger.info('Serializing preprocessed reviews')

# Serialize documents to new json file
preprocessed_file_path = 'resources/preprocessed_metacritic.json'

serialize_preprocessed_reviews(preprocessed_reviews, preprocessed_file_path)

logger.info('Preprocessed data saved to {}'.format(preprocessed_file_path))
