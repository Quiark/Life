from typing import List, Dict, Optional
from datetime import datetime
import config
from lib.data import Comment, Post, Group, User

# TODO: use the abc module
# store_X: just saves the thing in the database
# add_X: possibly does some further processing such as generating next id etc
class Database:
    
    def get_post(self, groupid: str, postid: str) -> Optional[Post]:
        pass

    def add_post(self, data: Post):
        now = datetime.utcnow()
        page = '{:04}{:02}'.format(now.year, now.month)

        # next
        ix = self._inc_postix(data.groupid, page)

        # figure out new id
        data.postid = '{}{:04}'.format(page, ix)

        self._store_post(data)
        return data

    # internal interface
    def _store_post(self, data: Post):
        pass


    def _inc_postix(self, groupid: str, page: str) -> int:
        pass


class MockDatabase(Database):
    def __init__(self):
        FIRST_GROUP = 'aaabb'
        SECOND_GROUP = 'zzz'
        self.posts = {}
        self.groups = {}
        self.users = {'admin': User('admin', 'Adminus', groups=[
            FIRST_GROUP,
            SECOND_GROUP,
            config.UNPUBLISHED_GROUP
            ], token='abcd_kocka_heslo')}

        self.g1 = Group(
                groupid=FIRST_GROUP,
                name='Family',
                pages={})

        self.g2 = Group(
                groupid=SECOND_GROUP,
                name='Kung-fu',
                pages={
                    '201701': 1,
                    '201702': 1,
                    '201704': 2,
                    '201601': 1,
                    })
        self.g3 = Group(
                groupid=config.UNPUBLISHED_GROUP,
                name='unpub',
                pages={})

        self.add_group(self.g1)
        self.add_group(self.g2)
        self.add_group(self.g3)

        self.p1 = Post(
            groupid=SECOND_GROUP,
            postid=None,
            comments=[],
            time=datetime.utcnow(),
            text='Travelling the world with my love'
        )

        self.p2 = Post(
            groupid=SECOND_GROUP,
            postid=None,
            comments=[
                Comment('gaga', 'hi', datetime.utcnow()),
                Comment('trollface', 'u mad', datetime.utcnow())
            ],
            time=datetime.now(),
            text='The other post'
        )

        self.mock_post(self.g2, '201701')
        self.mock_post(self.g2, '201702')
        self.mock_post(self.g2, '201704')
        self.mock_post(self.g2, '201704')
        self.mock_post(self.g1, '201601')

        self.add_post(self.p1)
        self.add_post(self.p2)
        self.add_comment(self.g1.groupid, self.p1.postid, Comment(author='admin', text='autocommnt'))

    def add_group(self, data: Group):
        self.groups[data.groupid] = data

    def get_group(self, groupid: str) -> Group:
        return self.groups[groupid]

    def get_groups(self) -> Optional[List[Group]]:
        return list(self.groups.values())

    def _inc_postix(self, groupid: str, page: str) -> int:
        ix = self.groups[groupid].pages.setdefault(page, 0)
        self.groups[groupid].pages[page] += 1
        return ix

    def _store_post(self, data: Post):
        # store post itself
        self.posts[data.postid] = data

    def mock_post(self, group: Group, page: str):
        post = Post(
                groupid=group.groupid,
                postid=page + '0000',
                comments=[],
                time=datetime.now(),
                text='Mock post, sorry if duplicate id')
        self.posts[post.postid] = post

    def get_post(self, groupid: str, postid: str) -> Post:
        return self.posts[postid]

    def get_posts_by_page(self, groupid: str, page: str) -> List[Post]:
        ids = filter(lambda it: (self.posts[it].page() == page) and (self.posts[it].groupid == groupid), self.posts)
        return [self.posts[x] for x in ids]

    def get_user(self, userid):
        return self.users[userid]

    def add_comment(self, groupid: str, postid: str, comment: Comment):
        p = self.posts[postid]
        p.comments.append(comment)
