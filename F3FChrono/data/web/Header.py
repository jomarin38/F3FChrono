from F3FChrono.data.web.Line import Line


class Header(Line):

    def __init__(self, name=None):
        super().__init__(name)
        self.tag = 'th'
