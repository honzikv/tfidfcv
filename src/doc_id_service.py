# Module for getting unique document ids
# Simply increments a counter and returns the next value

class IdService:
    def __init__(self):
        self.counter = -1

    def get_id(self):
        self.counter += 1
        return self.counter


doc_id_service = IdService()
