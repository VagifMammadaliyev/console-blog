class PageNotCompletedError(Exception):
    
    def __init__(self):
        self.message = 'PageNotCompletedError: This page is not completed.'