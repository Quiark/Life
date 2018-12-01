from typing import List, Dict
from datetime import datetime
import config
from lib.data import Comment, Post, Group, User

# TODO: use the abc module
class Database:
    
    def add_post(self, data: Post):
        pass

    def get_post(self, postid: str) -> Post:
        pass


class MockDatabase(Database):
    def __init__(self):
        self.posts = {}
        self.groups = {}
        self.users = {'admin': User('admin', 'Adminus', [
            config.FIRST_GROUP,
            'bugcp-kungfu'
            ])}

        self.g1 = Group(
                groupid=config.FIRST_GROUP,
                pages={'201601': 0})

        self.g2 = Group(
                groupid='bugcp-kungfu',
                pages={
                    '201701': 1,
                    '201702': 2,
                    '201704': 4,
                    '201705': 3,
                    '201802': 1,
                    })

        self.add_group(self.g1)
        self.add_group(self.g2)

        self.p1 = Post(
            groupid=config.FIRST_GROUP,
            postid=None,
            comments=[],
            time=datetime.utcnow(),
            text='Travelling the world with my love'
        )

        self.p2 = Post(
            groupid=config.FIRST_GROUP,
            postid=None,
            comments=[
                Comment('gaga', 'hi', datetime.utcnow()),
                Comment('trollface', 'u mad', datetime.utcnow())
            ],
            time=datetime.now(),
            text='The other post'
        )

        self.add_post(self.p1)
        self.add_post(self.p2)

    def add_group(self, data: Group):
        self.groups[data.groupid] = data

    def get_group(self, groupid: str) -> Group:
        return self.groups[groupid]

    def inc_postix(self, groupid: str, page: str) -> int:
        ix = self.groups[groupid].pages.setdefault(page, 0)
        self.groups[groupid].pages[page] += 1
        return ix

    def add_post(self, data: Post):
        now = datetime.utcnow()
        page = '{:04}{:02}'.format(now.year, now.month)

        # next
        ix = self.inc_postix(data.groupid, page)

        # figure out new id
        data.postid = '{}{:04}'.format(page, ix)

        # store post itself
        self.posts[data.postid] = data


    def get_post(self, postid: str) -> Post:
        return self.posts[postid]

    def get_posts_by_page(self, groupid: str, page: str) -> List[Post]:
        ids = filter(lambda it: self.posts[it].page() == page, self.posts)
        return [self.posts[x] for x in ids]

    def get_user(self, userid):
        return self.users[userid]
