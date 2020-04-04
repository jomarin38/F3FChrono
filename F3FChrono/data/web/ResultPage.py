import os

from F3FChrono.data.web.PageHeader import PageHeader


class ResultPage:

    css_string = None

    def __init__(self, title=None, event=None, f3f_round=None, authenticated=False):
        self.title = title
        self._header = PageHeader(event, f3f_round, authenticated)
        self._tables = []

    def set_title(self, title):
        self.title = title

    def add_table(self, table):
        self._tables.append(table)

    def to_html(self):
        res = "<html><head><meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">" + \
              "<style>" + ResultPage.get_css_string() + "</style></head><body>"
        res += self._header.to_html()
        res += '<h1>' + self.title + '</h1>'
        for table in self._tables:
            res += table.to_html()


        res+="</body></html>"
        return res

    @staticmethod
    def get_css_string():
        if ResultPage.css_string is None:
            ResultPage.css_string = ''
            css_path = os.path.realpath('F3FChrono/web/f3franking/static/event_view.css')
            try:
                with open(css_path) as fp:
                    lines = fp.readlines()
                    for line in lines:
                        ResultPage.css_string += line
            except:
                pass

        return ResultPage.css_string
