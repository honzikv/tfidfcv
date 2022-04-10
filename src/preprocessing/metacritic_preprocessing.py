import json
from datetime import datetime
from typing import List

from src.doc_id_service import doc_id_service
from src.metacritic_reviews import MetacriticReviewDocument


class MetacriticReview:

    def __init__(self, game_name: str, reviewer_name: str, date_reviewed: datetime, score: float, text: str,
                 is_critic_review: bool):
        self.game_name = game_name
        self.reviewer_name = reviewer_name
        self.date_reviewed = date_reviewed
        self.score = score
        self.text = text
        self.is_critic_review = is_critic_review


def map_review(json_review, is_critic_review, game_name):
    """
    Maps review from json to MetacriticReview object. Throws ValueException if the review is not valid.
    :param: json_review:  json review
    :param: is_critic_review: boolean indicating if the review is a critic review
    :return:
    """
    reviewer_name = json_review['reviewerName']
    score = float(json_review['score'])
    date_reviewed = datetime.strptime(json_review['dateReviewed'], '%b %d, %Y')
    text = json_review['text']

    return MetacriticReview(game_name, reviewer_name, date_reviewed, score, text, is_critic_review)


def load_metacritic_reviews(file_path) -> List[MetacriticReview]:
    """
    Loads reviews from crawled json file and maps it to "domain" objects
    :param: file_path:
    :return: list of MetacriticReview objects
    """

    reviews = []
    with open(file_path, 'r', encoding='utf-8') as f:
        # Read the json contents
        file = json.load(f)

        # Iterate over the json contents
        for year in file:
            for game in file[year]:
                # Get the game name
                game_name = game['name']
                # Get the critic reviews
                critic_reviews = game['critic_reviews']
                # Get the user reviews
                user_reviews = game['userReviews']

                # Iterate over the critic reviews
                for review in critic_reviews:
                    reviews.append(map_review(review, True, game_name))

                for review in user_reviews:
                    reviews.append(map_review(review, False, game_name))

        return reviews


def serialize_unpreprocessed_metacritic_reviews(reviews: List[MetacriticReview], file_path):
    """
    Serializes the reviews to json format
    :param reviews: list of MetacriticReview objects
    :param file_path:
    :return:
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([obj.__dict__ for obj in reviews], f, indent=4, default=str, sort_keys=True)


def preprocess_reviews(metacritic_reviews: List[MetacriticReview], preprocessor):
    """
    Preprocesses the reviews.
    :param: metacritic_reviews:
    :param: file_path:
    :return:
    """
    reviews = []
    for review in metacritic_reviews:
        try:
            tokens = preprocessor.get_processed_tokens(review.text)
        except ValueError:  # if we get value error the language was not recognized
            continue

        doc_id = doc_id_service.get_id()
        reviews.append(
            MetacriticReviewDocument(doc_id, tokens, review.game_name, review.reviewer_name, review.date_reviewed,
                                     review.score, review.text, review.is_critic_review))

    return reviews


def serialize_preprocessed_reviews(reviews: List[MetacriticReviewDocument], file_path):
    """
    Serializes the preprocessed reviews to json format
    :param reviews: list of MetacriticReviewDocument objects
    :param file_path:
    :return:
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([obj.__dict__ for obj in reviews], f, indent=4, default=str, sort_keys=True)
