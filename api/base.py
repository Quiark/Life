from jinja2 import Template
from jinja2 import Environment, FileSystemLoader, select_autoescape
import config
from lib.storage import LocalStorage
from lib.posts import PostCreator

jinja = Environment(
    loader=FileSystemLoader(config.TEMPLATES),
    autoescape=select_autoescape(['html', 'xml'])
)

storage = LocalStorage()

pc = PostCreator(jinja, storage, config.FIRST_GROUP, 'abc1.jpg')

