from fastapi import FastAPI

from src.api.dtos import CosineSearchDto
from src.cosine_similarity import CosineSimilaritySearch
from src.logging import logger_factory

MAX_SEARCH_ITEMS = 10_000

logger = logger_factory.get_logger(__name__)
port = 8000


def start_api(cos_sim_model: CosineSimilaritySearch):
    app = FastAPI()

    # Sample test endpoint
    @app.get("/")
    def root():
        return {"message": "Hello World"}

    @app.post("/cosine_search/")
    def cosine_search(cosine_search_req: CosineSearchDto):
        if cosine_search_req.limit > MAX_SEARCH_ITEMS:
            return {'success': False,
                    'message': f'Requested limit ({cosine_search_req.limit}) exceeds maximum ({MAX_SEARCH_ITEMS})'}

        search_results = cos_sim_model.get_top_n_documents(cosine_search_req.query, cosine_search_req.limit)
        return search_results

    logger.info(f'Starting API server on http://localhost:{port}')

