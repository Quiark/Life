from datetime import datetime
import config
from lib.data import Comment, Post

# TODO: use the abc module
class Database:
    
    def save_post(self, data: Post):
        pass

    def get_post(self, postid: str) -> Post:
        pass


class MockDatabase(Database):
    def __init__(self):
        self.store = {}

        self.p1 = Post(
            groupid=config.FIRST_GROUP,
            postid='2018110001',
            comments=[],
            time=datetime.utcnow(),
            text='Travelling the world with my love'
        )

        self.p2 = Post(
            groupid=config.FIRST_GROUP,
            postid='2018100001',
            comments=[
                Comment('gaga', 'hi', datetime.utcnow()),
                Comment('trollface', 'u mad', datetime.utcnow())
            ],
            time=datetime.now(),
            text='The other post'
        )

        self.save_post(self.p1)
        self.save_post(self.p2)

    def save_post(self, data: Post):
        self.store[data.postid] = data

    def get_post(self, postid: str) -> Post:
        return self.store[postid]
