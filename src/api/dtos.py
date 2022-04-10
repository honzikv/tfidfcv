from pydantic import BaseModel


class CosineSearchDto(BaseModel):
    query: str
    limit: int = 10
    offset: int = 0
