from django.http import HttpResponse
from F3FChrono.data.dao.EventDAO import EventDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO
from F3FChrono.data.web.HTMLText import HTMLText
from F3FChrono.data.web.ResultPage import ResultPage
from F3FChrono.data.web.ResultTable import ResultTable
from F3FChrono.data.web.Header import Header
from F3FChrono.data.web.Line import Line
from F3FChrono.data.web.Cell import Cell
from F3FChrono.data.web.Link import Link
from F3FChrono.data.web.Utils import Utils
from django.views.decorators.cache import never_cache
import datetime

@never_cache
def is_alive(request):
    return HttpResponse('<p>Hello world !</p>')


@never_cache
def index(request):

    Utils.set_port_number(request.META['SERVER_PORT'])

    dao = EventDAO()

    events = dao.get_list()

    page = ResultPage(title='Events list')

    table = ResultTable(title='', css_id='ranking')

    header = Header(name=Cell('Name'))
    header.add_cell(Cell('Location'))
    header.add_cell(Cell('Begin date'))
    header.add_cell((Cell('End date')))
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


@never_cache
def event_view(request):

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')

    return HttpResponse(event_view_html(event_id))

def get_cell_css_id(competitor_rank):
    if competitor_rank==1:
        return 'first'
    elif competitor_rank==2:
        return 'second'
    elif competitor_rank==3:
        return 'third'
    else:
        return None


def event_view_html(event_id):

    event = EventDAO().get(event_id=event_id, fetch_competitors=True, fetch_rounds=True, fetch_runs=True)

    page = ResultPage(title=event.name)

    if event.has_ongoing_round():
        table = ResultTable('Ongoing round :', css_id='ranking')
        header = Header(name=Link('Round ' + str(len(event.valid_rounds)+1),
                                  'round_view?event_id=' + str(event_id) +
                                  '&round_number=' + str(event.get_current_round().round_number)))
        table.set_header(header)
        page.add_table(table)

    if len(event.valid_rounds) > 0:
        event.compute_ranking()

        warning = HTMLText('WARNING : These results are not official. '
                           'They are based on raw data and does not have been validated')

        page.add_text(warning)

        #Evolutive ranking table
        table = ResultTable(title='Evolutive ranking', css_id="ranking")
        header = Header(name=Cell('Rank'))
        header.add_cell(Cell('Bib'))
        header.add_cell(Cell('Points'))
        header.add_cell(Cell('Points / 1000'))
        header.add_cell(Cell('Name'))
        for f3f_round in event.valid_rounds:
            header.add_cell(Link(f3f_round.display_name(),
                                 'round_view?event_id=' + str(event_id) +
                                 '&round_number=' + str(f3f_round.round_number)))
        table.set_header(header)

        best_score = None
        for competitor in sorted([competitor for bib, competitor in event.competitors.items()], key=lambda c: c.rank):
            row = Line(name=Cell('{:2d}'.format(int(competitor.rank))))
            row.add_cell(Cell(str(competitor.bib_number)))
            competitor_score = competitor.score_with_jokers(len(event.valid_rounds))
            row.add_cell(Cell('{:6.2f}'.format(competitor_score)))
            if best_score is None:
                best_score = competitor_score
            row.add_cell(Cell('{:2d}'.format(int(competitor_score / best_score * 1000))))
            row.add_cell(Cell(competitor.pilot.to_string()))
            for f3f_round in event.valid_rounds:
                competitor_rank = int(competitor.evolutive_rank[f3f_round.valid_round_number-1])
                row.add_cell(Cell('{:2d}'.format(competitor_rank), css_id=get_cell_css_id(competitor_rank)))
            table.add_line(row)

        page.add_table(table)

        # Round scores table
        table = ResultTable(title='Round scores', css_id="ranking")
        header = Header(name=Cell('Bib'))
        header.add_cell(Cell('Name'))
        for f3f_round in event.rounds:
            if f3f_round.valid:
                header.add_cell(Link(f3f_round.display_name(),
                                     'round_view?event_id=' + str(event_id) +
                                     '&round_number=' + str(f3f_round.round_number)))
        table.set_header(header)

        for competitor in sorted([competitor for bib, competitor in event.competitors.items()], key=lambda c: c.bib_number):
            row = Line(name=Cell(str(competitor.bib_number)))
            row.add_cell(Cell(competitor.pilot.to_string()))
            for f3f_round in event.valid_rounds:
                round_group = f3f_round.find_group(competitor)
                if round_group is not None:
                    run = round_group.get_valid_run(competitor)
                    if run is None:
                        score = 0
                    else:
                        score = run.score
                else:
                    score = 0
                winner = score >= 1000
                joker = (event.number_of_valid_rounds >= event.first_joker_round_number and
                         f3f_round.valid_round_number == competitor.first_joker_round_number) \
                        or \
                        (event.number_of_valid_rounds >= event.second_joker_round_number and
                         f3f_round.valid_round_number == competitor.second_joker_round_number)

                row.add_cell(Cell('{:2d}'.format(int(score)), joker=joker, winner=winner))
            table.add_line(row)

        page.add_table(table)

    result = page.to_html()

    return result


@never_cache
def round_view(request):

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    round_number = request.GET.get('round_number')

    return HttpResponse(round_view_html(event_id, round_number))


def round_view_html(event_id, round_number):

    f3f_round = RoundDAO().get_from_ids(event_id, round_number, fetch_runs=True)

    page = ResultPage(title=f3f_round.event.name + '\t' + f3f_round.display_name() +
                            '(id:' + str(f3f_round.round_number) + ')', event=f3f_round.event)

    best_runs = f3f_round.get_best_runs()
    best_runs_string = 'Best time : <br>'

    for run in best_runs:
        if run is not None:
            best_runs_string += run.to_string()

    table = ResultTable(title=best_runs_string, css_id='ranking')
    header = Header(name=Cell('Bib'))
    header.add_cell(Cell('Group'))
    header.add_cell(Cell('Name'))
    header.add_cell(Cell('Flight time'))
    header.add_cell(Cell('Score'))
    table.set_header(header)

    #Later loop on rounds and round groups
    round_group = f3f_round.groups[0]
    for round_group in f3f_round.groups:
        round_group.compute_scores()
        for competitor in sorted(round_group.runs):
            row = Line(name=Cell(str(competitor.bib_number)))
            row.add_cell(Cell(str(round_group.group_number)))
            row.add_cell(Cell(competitor.pilot.to_string()))
            row.add_cell(Cell(round_group.run_value_as_string(competitor)))
            row.add_cell(Cell(str(round_group.run_score_as_string(competitor))))
            table.add_line(row)

    page.add_table(table)

    table = ResultTable(title='Remaining pilots to fly', css_id='ranking')
    header = Header(name=Cell('Bib'))
    header.add_cell(Cell('Group'))
    header.add_cell(Cell('Name'))
    table.set_header(header)

    for bib_number in f3f_round.get_remaining_bibs_to_fly():
        row = Line(name=Cell(str(bib_number)))
        row.add_cell(Cell(str(f3f_round.find_group(f3f_round.event.competitors[bib_number]).group_number)))
        row.add_cell(Cell(f3f_round.event.competitors[bib_number].display_name()))
        table.add_line(row)

    page.add_table(table)

    result = page.to_html()
    return result


if __name__ == "__main__":
    # execute only if run as a script
    event_view_html(1)
    #round_view_html(1, 21)


