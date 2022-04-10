# Module for reading metacritic reviews from the documents.json file
from datetime import datetime
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

    def __str__(self):
        return f"""
        {super().__str__()}
        MetacriticReviewDocument
            text: {self.text}
            reviewer_name: {self.reviewer_name}
            date_reviewed: {self.dateReviewed}
            score: {self.score}
            game_name: {self.gameName}
            is_critic_review: {self.criticReview}"""


