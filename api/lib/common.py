from datetime import datetime
import pytz

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
    return t.strftime('%I:%M, %d.%m.%Y')
