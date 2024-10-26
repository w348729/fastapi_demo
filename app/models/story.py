from typing import Optional
from pydantic import BaseModel


class Story(BaseModel):
    title: str
    content: str
    author: str
    country: str

    class Config:
        schema_extra = {
            'example': {
                'title': 'abc',
                'content': 'efghj',
                'autho': 'aa',
                'country': 'cn'
            }
        }


class StoryUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    author: Optional[str]
    country: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                'title': 'cba',
                'content': 'ghjyt',
                'author': 'ee',
                'country': 'cnhhhh'
            }
        }
