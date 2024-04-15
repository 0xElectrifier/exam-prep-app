class ApplicationError(Exception):

    def __init__(self, *args, **kwargs):
        # super().__init__(message)

        self.message = kwargs.get('message')
        if not self.message:
            self.message = ""
        self.errors = kwargs.get('errors')
        if not self.errors:
            self.errors = {}
        self.status_code = kwargs.get('status_code')
        if not self.status_code:
            self.status_code = 400
