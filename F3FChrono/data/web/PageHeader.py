from F3FChrono.data.web.ResultTable import ResultTable
from F3FChrono.data.web.Header import Header
from F3FChrono.data.web.Link import Link
from F3FChrono.data.web.Utils import Utils


class PageHeader:

    def __init__(self, event=None, f3f_round=None, authenticated=False):

        self._base_url = Utils.get_base_url()

        self._table = ResultTable(title='', css_id='header')
        header = Header(name=Link('Back to events list', self._base_url))
        if event is not None:
            header.add_cell(Link('Back to event view', self._base_url + '/event_view?event_id=' + str(event.id)))
        if authenticated:
            header.add_cell(Link('Log out', Utils.get_logout_url()))
        self._table.set_header(header)

    def to_html(self):
        return self._table.to_html()
