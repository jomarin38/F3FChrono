from F3FChrono.data.web.Cell import Cell

class Link(Cell):

    def __init__(self, value, url):
        super().__init__(value)
        self.url = url

    def to_html(self):
        return '<a href=\"'+self.url+'\">'+self.value+'</a>'
