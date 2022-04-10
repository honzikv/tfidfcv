from fastapi import FastAPI

from src.api.dtos import CosineSearchDto
from src.cosine_similarity import build_cos_similarity_model
from src.logging import logger_factory
from src.preprocessing.metacritic_preprocessing import deserialize_unpreprocessed_metacritic_reviews, preprocess_reviews
from src.preprocessing.preprocessor import metacritic_preprocessor
from src.api.api import start_api

logger = logger_factory.get_logger(__name__)


def get_documents():
    """
    Gets all documents to be indexed
    :return:
    """
    metacritic_documents_path = 'resources/unpreprocessed_reviews.json'
    logger.info('Getting documents from {}'.format(metacritic_documents_path))
    unpreproc_docs = deserialize_unpreprocessed_metacritic_reviews(metacritic_documents_path)

    logger.info('Preprocessing documents')
    return preprocess_reviews(unpreproc_docs, metacritic_preprocessor)


logger.info('Starting the application')

metacritic_reviews = get_documents()
logger.info('Documents loaded, building cosine similarity model')
cos_model = build_cos_similarity_model(metacritic_reviews, metacritic_preprocessor)

logger.info('Starting the API')

app = FastAPI()

MAX_SEARCH_ITEMS = 10_000

port = 8000


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/cosine_search/")
def cosine_search(cosine_search_req: CosineSearchDto):
    if cosine_search_req.limit > MAX_SEARCH_ITEMS:
        return {'success': False,
                'message': f'Requested limit ({cosine_search_req.limit}) exceeds maximum ({MAX_SEARCH_ITEMS})'}

    search_results = cos_model.get_top_n_documents(cosine_search_req.query, cosine_search_req.limit)
    return search_results


logger.info(f'Starting API server on http://localhost:{port}')

app.setup()