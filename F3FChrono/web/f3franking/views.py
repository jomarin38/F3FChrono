from django.http import HttpResponse
from F3FChrono.data.dao.EventDAO import EventDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO
from F3FChrono.data.web.TableResultPage import TableResultPage
from F3FChrono.data.web.Header import Header
from F3FChrono.data.web.Line import Line
from F3FChrono.data.web.Cell import Cell
from F3FChrono.data.web.Link import Link


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

    return HttpResponse(event_view_html(event_id))

def event_view_html(event_id):

    event = EventDAO().get(event_id=event_id, fetch_competitors=True, fetch_rounds=True, fetch_runs=True)

    page = TableResultPage(title=event.name)
    header = Header(name=Cell('Rank'))
    header.add_cell(Cell('Bib'))
    header.add_cell(Cell('Points'))
    header.add_cell(Cell('Name'))
    for f3f_round in event.rounds:
        header.add_cell(Link('Round ' + str(f3f_round.round_number),
                             'round_view?event_id=' + str(event_id) +
                             '&round_number=' + str(f3f_round.round_number)))
    page.set_header(header)

    event.compute_ranking()

    #Later loop on rounds and round groups
    for competitor in sorted([competitor for bib, competitor in event.competitors.items()], key=lambda c: c.rank):
        row = Line(name=Cell(str(competitor.rank)))
        row.add_cell(Cell(str(competitor.bib_number)))
        row.add_cell(Cell(str(competitor.score)))
        row.add_cell(Cell(competitor.pilot.to_string()))
        for f3f_round in event.rounds:
            round_group = f3f_round.groups[0]
            row.add_cell(Cell(str(competitor.rank)))
        page.add_line(row)

    result = page.to_html()
    return result


def round_view(request):

    event_id = request.GET.get('event_id')
    round_number = request.GET.get('round_number')

    return HttpResponse(round_view_html(event_id, round_number))


def round_view_html(event_id, round_number):

    f3f_round = RoundDAO().get_from_ids(event_id, round_number, fetch_runs=True)

    page = TableResultPage(title=f3f_round.event.name + '\tRound : ' + str(f3f_round.round_number))
    header = Header(name=Cell('Bib'))
    header.add_cell(Cell('Name'))
    header.add_cell(Cell('Flight time'))
    header.add_cell(Cell('Score'))
    page.set_header(header)

    #Later loop on rounds and round groups
    round_group = f3f_round.groups[0]
    round_group.compute_scores()
    for competitor in sorted(round_group.runs):
        row = Line(name=Cell(str(competitor.bib_number)))
        row.add_cell(Cell(competitor.pilot.to_string()))
        row.add_cell(Cell(round_group.run_value_as_string(competitor)))
        row.add_cell(Cell(str(round_group.run_score_as_string(competitor))))
        page.add_line(row)

    result = page.to_html()
    return result


if __name__ == "__main__":
    # execute only if run as a script
    event_view_html(1)


