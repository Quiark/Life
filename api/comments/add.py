import lib.http

class ActualHandler:
    def get(self):
        return {'note': 'totally added a comment'}

class handler(lib.http.GenericHandler):
    actual = ActualHandler()
