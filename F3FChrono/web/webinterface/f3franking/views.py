from django.http import HttpResponse
from F3FChrono.data.dao.EventDAO import EventDAO


def index(request):

    dao = EventDAO()

    events = dao.get_list()

    result = '<h1>Events list</h1>\n'

    result += '<table>\n'
    result += '<thead><tr><th>Name</th><th>Location</th><th>Begin date</th><th>End Date</th></tr></thead>\n'
    result += '<tbody>'
    for event in events:
        fetched_event = dao.get(event.id)
        result += '<tr><td><a href=\"event_view?event_id=' + str(fetched_event.id) + '\">'+fetched_event.name + \
                  '</a></td><td>' + \
                  fetched_event.location + '</td><td>' + \
                  str(fetched_event.begin_date) + '</td><td>' + \
                  str(fetched_event.end_date) + '</td></tr>'

    result += '</tbody></table>\n'

    return HttpResponse(result)

def event_view(request):

    event_id = request.GET.get('event_id')

    event = EventDAO().get(event_id=event_id, fetch_competitors=True, fetch_rounds=True, fetch_runs=True)

    result = '<h1>' + event.name + '</h1>'

    result += '<p>Number of competitors : ' + str(len(event.get_competitors())) + '</p>'
    result += '<p>Number of rounds : ' + str(len(event.rounds)) + '</p>'


    return HttpResponse(result)

