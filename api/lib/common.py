import os
from datetime import datetime
import pytz

import config

def first(m):
    # for iterators
    return list(m)[0]

def lstrip_if(fr: str, prefix: str) -> str:
    if fr.startswith(prefix):
        return fr[len(prefix):]
    else:
        return fr

def display_timestamp(utcstamp: datetime) -> str:
    tz = pytz.timezone('Asia/Hong_Kong')  # TODO get timezone from user
    t = utcstamp.astimezone(tz)
    return t.strftime('%I:%M, %d. %m. %Y')

def aws_api_args() -> dict:
    if config.API_LOCAL:
        return {}
    else: 
        return {
            'aws_access_key_id': os.environ['API_ACCESS_KEY_ID'],
            'aws_secret_access_key': os.environ['API_SECRET_ACCESS_KEY']
        }
