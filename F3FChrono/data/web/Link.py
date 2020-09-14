from F3FChrono.data.web.Cell import Cell

class Link(Cell):

    def __init__(self, value, url, new_tab=False):
        super().__init__(value)
        self.url = url
        self.new_tab = new_tab

    def to_html(self):
        result = '<a href=\"'+self.url+'\"'
        if self.new_tab:
            result += ' target=\"_blank\"'
        result += '>'+self.value+'</a>'
        return result
