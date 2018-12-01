from datetime import datetime
from typing import List, Dict
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

@dataclass
class Group:
    groupid: str

    # pageid -> next id of post
    # pageid is 201804 for april of 2018
    pages: Dict[str, int]

    colour: str = 'blue'

@dataclass
class User:
    userid: str
    name: str

    groups: List[Group]
