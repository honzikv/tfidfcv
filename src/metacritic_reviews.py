# Module for reading metacritic reviews from the documents.json file
import json
from datetime import datetime
from typing import List

from src.doc_id_service import doc_id_service
from src.document import Document


class MetacriticReviewDocument(Document):

    def __init__(self, doc_id, terms, game_name: str, reviewer_name: str, date_reviewed: datetime, score: float,
                 text: str,
                 criticReview: bool):
        super().__init__(doc_id, terms)
        self.gameName = game_name
        self.reviewer_name = reviewer_name
        self.dateReviewed = date_reviewed
        self.score = score
        self.text = text
        self.criticReview = criticReview


def read_metacritic_reviews(json_path: str) -> List[MetacriticReviewDocument]:
    """
    Reads the metacritic reviews from the json file.
    :param: json_path: path to the json file
    :return:
    """
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
        metacritic_reviews = []
        for review in json_data:
            game_name = review['gameName']
            reviewer_name = review['reviewer_name']
            date_reviewed = datetime.fromtimestamp(review['dateReviewed'])
            score = review['score']
            text = review['text']
            critic_review = review['criticReview']
            doc_id = doc_id_service.get_id()
            terms = text.split(' ')
            metacritic_reviews.append(
                MetacriticReviewDocument(doc_id, terms, game_name, reviewer_name, date_reviewed, score, text,
                                         critic_review))
