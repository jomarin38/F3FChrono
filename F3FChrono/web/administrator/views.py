from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.cache import never_cache

from F3FChrono.data.dao.EventDAO import EventDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO
from F3FChrono.data.web.ResultPage import ResultPage
from F3FChrono.data.web.ResultTable import ResultTable
from F3FChrono.data.web.Header import Header
from F3FChrono.data.web.Line import Line
from F3FChrono.data.web.Cell import Cell
from F3FChrono.data.web.Link import Link
from F3FChrono.data.web.Utils import Utils


def sign_in(request):
    if not request.user.is_authenticated:

        return render(request, 'login_template.html', {})

    else:
        return HttpResponse('Authenticated user !')


def login_f3f_admin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect('index')
    else:
        return redirect('sign_in')


def logout_f3f_admin(request):
    logout(request)
    return HttpResponse('<p>Successfully logged out !</p>')


@never_cache
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    dao = EventDAO()

    events = dao.get_list()

    page = ResultPage(title='F3F RACE MNGT Administration', authenticated=request.user.is_authenticated)

    table = ResultTable(title='', css_id='ranking')

    header = Header(name=Cell('Create new event'))
    table.set_header(header)

    page.add_table(table)

    table = ResultTable(title='Manage existing event', css_id='ranking')

    header = Header(name=Cell('Event Name'))
    table.set_header(header)

    for event in events:
        fetched_event = dao.get(event.id)
        row = Line(name=Link(fetched_event.name, 'event_view?event_id=' + str(fetched_event.id)))
        row.add_cell(Cell(fetched_event.location))
        row.add_cell(Cell(str(fetched_event.begin_date)))
        row.add_cell(Cell(str(fetched_event.end_date)))
        table.add_line(row)

    page.add_table(table)

    return HttpResponse(page.to_html())


if __name__ == "__main__":
    # execute only if run as a script
    pass
    #round_view_html(1, 21)

