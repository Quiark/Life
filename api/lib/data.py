from datetime import datetime
from typing import List
from dataclasses import dataclass

# this is as stored in DynamoDB

@dataclass
class Comment:
    ix: int
    author: str
    text: str
    time: datetime = datetime.utcnow()

# TODO what are the keys and what are the indexes?
@dataclass
class Post:
    groupid: str
    # refers to image on S3 but not gettable by id
    postid: str
    # yes?
    text: str
    comments: List[Comment]
    time: datetime = datetime.utcnow()

    def page(self) -> str:
        return self.postid[:6]


