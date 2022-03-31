#
# This file is part of the F3FChrono distribution (https://github.com/jomarin38/F3FChrono).
# Copyright (c) 2021 Sylvain DAVIET, Joel MARIN.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template import RequestContext
from django.views.decorators.cache import never_cache

from F3FChrono.data.Chrono import Chrono
from F3FChrono.data.Run import Run
from F3FChrono.data.dao.CompetitorDAO import CompetitorDAO
from F3FChrono.data.dao.EventDAO import EventDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO
from F3FChrono.data.web.ResultPage import ResultPage
from F3FChrono.data.web.ResultTable import ResultTable
from F3FChrono.data.web.Header import Header
from F3FChrono.data.web.Line import Line
from F3FChrono.data.web.Cell import Cell
from F3FChrono.data.web.Link import Link
from F3FChrono.data.web.Utils import Utils
from F3FChrono.data.Event import Event
from F3FChrono.data.Pilot import Pilot
from F3FChrono.data.Round import Round

import csv


def sign_in(request):
    if not request.user.is_authenticated:

        return render(request, 'login_template.html',
                                  {'next' : request.GET.get('next')}
                                  )

    else:
        return HttpResponse('Authenticated user !')


def login_f3f_admin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect(request.GET.get('next'))
    else:
        return redirect('sign_in')


def logout_f3f_admin(request):
    logout(request)
    return HttpResponse('<p>Successfully logged out !</p>')


def create_new_event(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    return render(request, 'new_event_template.html', {})


def new_pilot_input(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    return render(request, 'new_pilot_template.html', {'event_id': request.GET.get('event_id')})


def set_time(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    return render(request, 'edit_time_template.html', {'event_id': request.GET.get('event_id'),
                                                       'round_number': request.GET.get('round_number'),
                                                       'bib_number': request.GET.get('bib_number')})


def cancel_round(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET['event_id']
    round_number = request.GET['round_number']

    f3f_round = RoundDAO().get_from_ids(event_id, round_number, fetch_runs=True)
    f3f_round.do_cancel_round()

    return HttpResponseRedirect('manage_event?event_id='+event_id)


def validate_round(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET['event_id']
    round_number = request.GET['round_number']

    f3f_round = RoundDAO().get_from_ids(event_id, round_number, fetch_runs=True)
    f3f_round.validate_round(insert_database=True)

    return HttpResponseRedirect('manage_event?event_id='+event_id)


def register_new_pilot(request):

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    pilot_name = request.POST['pilotname']
    pilot_first_name = request.POST['pilotfirstname']
    pilot_fai_id = request.POST['pilotfaiid']
    pilot_national_id = request.POST['pilotnationalid']
    pilot_f3xvault_id = request.POST['pilotf3xvaultid']

    event_id = request.GET.get('event_id')
    event = EventDAO().get(event_id, fetch_competitors=True)

    pilot = Pilot(name=pilot_name,
                  first_name=pilot_first_name,
                  f3x_vault_id=pilot_f3xvault_id,
                  national_id=pilot_national_id,
                  fai_id=pilot_fai_id
                  )

    bib_number = event.next_available_bib_number()

    competitor = event.register_pilot(pilot, bib_number)
    CompetitorDAO().insert(competitor)

    return HttpResponseRedirect('manage_event?event_id='+event_id)


def edit_run_time(request):

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    flight_time = float(request.POST['flight_time'])

    event_id = int(request.GET.get('event_id'))
    round_number = int(request.GET.get('round_number'))
    bib_number = int(request.GET.get('bib_number'))

    event = EventDAO().get(event_id, fetch_competitors=True)
    f3f_round = RoundDAO().get_from_ids(event_id, round_number, fetch_runs=True)

    chrono = Chrono()
    chrono.run_time = flight_time

    run = Run()
    run.competitor = event.get_competitor(bib_number)
    run.penalty = 0
    run.chrono = chrono
    run.valid = True

    f3f_round.add_run_from_web(run)

    RoundDAO().update(f3f_round)

    return HttpResponseRedirect('manage_round?event_id='+str(event_id)+'&round_number='+str(round_number))


def delete_event(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    return render(request, 'event_deletion_template.html', {'event_id': request.GET.get('event_id')})


def do_delete_event(request):

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    EventDAO().delete(EventDAO().get(event_id))

    return redirect('index')


def load_from_f3x_vault(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    if ('username' in request.POST) and ('password' in request.POST) and ('F3X_vault_id' in request.POST):

        f3x_username = request.POST["username"]
        f3x_password = request.POST["password"]

        f3x_event_id = request.POST["F3X_vault_id"]

        event = Event.from_f3x_vault(f3x_username, f3x_password, f3x_event_id)

        event.id = EventDAO().insert(event)

        for bib, competitor in event.get_competitors().items():
            CompetitorDAO().insert(competitor)

        for f3f_round in event.rounds:
            RoundDAO().insert(f3f_round)

        return redirect('index')

    else:

        return HttpResponse('<p>Invalid parameters !')


def load_from_scratch(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])
    try:
        csv_file = request.FILES["csv_file"]
        event_name = request.POST["eventname"]
        event_location = request.POST["eventlocation"]
        event_start_date = request.POST["startdate"]
        event_end_date = request.POST["enddate"]

        event = Event.from_csv(event_name, event_location, event_start_date, event_end_date, csv_file)

        event.id = EventDAO().insert(event)

        for bib, competitor in event.get_competitors().items():
            CompetitorDAO().insert(competitor)

        return redirect('index')

    except Exception as e:
        return HttpResponse('<p>Invalid parameters !')


def manage_event(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')

    event = EventDAO().get(event_id=event_id, fetch_competitors=True, fetch_rounds=True, fetch_runs=True)

    page = ResultPage(title=event.name, authenticated=request.user.is_authenticated)

    table = ResultTable(title='', css_id='ranking')

    header = Header(name=Link('Delete event', 'delete_event?event_id='+event_id))
    table.set_header(header)

    page.add_table(table)

    table = ResultTable(title='', css_id='ranking')

    header = Header(name=Link('Export bib numbers', 'download_pilots_as_csv?event_id=' + event_id))
    table.set_header(header)

    page.add_table(table)

    table = ResultTable(title='', css_id='ranking')

    header = Header(name=Link('Define bib numbers', 'define_bibs?event_id='+event_id))
    table.set_header(header)

    page.add_table(table)

    table = ResultTable(title='', css_id='ranking')

    header = Header(name=Link('Export to F3X Vault', 'login_to_export_event_f3x_vault?event_id='+event_id))
    table.set_header(header)

    page.add_table(table)

    table = ResultTable(title='Pilots', css_id="ranking")
    header = Header(name=Cell('Bib'))
    header.add_cell(Cell('Name'))
    header.add_cell(Cell(''))
    header.add_cell(Cell(''))
    table.set_header(header)

    for competitor in sorted([competitor for bib, competitor in event.competitors.items()], key=lambda c: c.bib_number):
        row = Line(name=Cell(str(competitor.bib_number)))
        row.add_cell(Cell(competitor.display_name()))
        if not event.has_run_competitor(competitor):
            row.add_cell(Link('Remove', 'remove_competitor?event_id='+str(event.id)+
                              '&bib_number='+str(competitor.bib_number)))
        else:
            row.add_cell(Cell(''))
        if competitor.present:
            row.add_cell(Link('Set not present', 'set_competitor_presence?event_id='+str(event.id)+
                              '&bib_number='+str(competitor.bib_number)+'&present=0'))
        else:
            row.add_cell(Link('Set present', 'set_competitor_presence?event_id=' + str(event.id) +
                              '&bib_number=' + str(competitor.bib_number)+'&present=1'))
        table.add_line(row)
    page.add_table(table)

    table = ResultTable(title='', css_id='ranking')

    header = Header(name=Link('Add new pilot', 'new_pilot_input?event_id='+event_id))
    table.set_header(header)

    page.add_table(table)

    table = ResultTable(title='Rounds', css_id="ranking")
    header = Header(name=Cell('Round number'))
    header.add_cell(Cell(''))
    header.add_cell(Cell(''))
    header.add_cell(Cell(''))
    header.add_cell(Cell(''))
    table.set_header(header)

    for f3f_round in event.rounds:
        row = Line(name=Link(str(f3f_round.display_name()), 'manage_round?event_id=' +
                             str(event.id)+'&round_number='+str(f3f_round.round_number), new_tab=True))
        row.add_cell(Link('Export to csv', 'download_csv?event_id=' + str(event.id) +
                          '&round_number='+str(f3f_round.round_number)))
        row.add_cell(Link('Export to F3XVault', 'login_to_export_round_f3x_vault?event_id=' + str(event.id) +
                          '&round_number='+str(f3f_round.round_number)))
        row.add_cell(Link('Cancel Round', 'cancel_round?event_id=' + str(event.id) +
                          '&round_number=' + str(f3f_round.round_number)))
        if f3f_round.valid:
            row.add_cell(Cell(''))
        else:
            row.add_cell(Link('Validate Round', 'validate_round?event_id=' + str(event.id) +
                              '&round_number='+str(f3f_round.round_number)))
        table.add_line(row)
    page.add_table(table)

    return HttpResponse(page.to_html())


def define_bibs(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    return render(request, 'define_bibs_template.html', {'event_id': request.GET.get('event_id')})

def do_define_bibs(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')

    csv_file = request.FILES["csv_file"]

    event = EventDAO().get(event_id, fetch_competitors=True, fetch_rounds=False, fetch_runs=False)

    event.import_bibs(csv_file)

    for bib, competitor in event.get_competitors().items():
        CompetitorDAO().update(competitor)

    if ('username' in request.POST) and ('password' in request.POST):

        f3x_username = request.POST["username"]
        f3x_password = request.POST["password"]

        if len(f3x_username)>0 and len(f3x_password)>0:
            event.export_bibs_to_f3xvault(f3x_username, f3x_password)

    return HttpResponseRedirect('manage_event?event_id=' + event_id)

def login_to_export_round_f3x_vault(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    return render(request, 'round_f3x_vault_export_template.html',
                  {'event_id': request.GET.get('event_id'), 'round_number': request.GET.get('round_number')})


def export_round_f3x_vault(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    round_number = request.GET.get('round_number')

    if ('username' in request.POST) and ('password' in request.POST):

        f3x_username = request.POST["username"]
        f3x_password = request.POST["password"]

        #We must fetch full event to get correct valid round number
        event = EventDAO().get(event_id, fetch_competitors=True, fetch_rounds=True, fetch_runs=True)
        requested_f3f_round = None
        for f3f_round in event.rounds:
            if f3f_round.round_number == int(round_number):
                requested_f3f_round = f3f_round

        if requested_f3f_round is not None:
            requested_f3f_round.export_to_f3x_vault(f3x_username, f3x_password)

    return HttpResponseRedirect('manage_event?event_id=' + event_id)


def login_to_export_event_f3x_vault(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    return render(request, 'event_f3x_vault_export_template.html',
                  {'event_id': request.GET.get('event_id')})


def export_event_f3x_vault(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')

    if ('username' in request.POST) and ('password' in request.POST):

        f3x_username = request.POST["username"]
        f3x_password = request.POST["password"]

        event = EventDAO().get(event_id, fetch_competitors=True, fetch_rounds=True, fetch_runs=True)
        event.export_to_f3x_vault(f3x_username, f3x_password)

    return HttpResponseRedirect('manage_event?event_id=' + event_id)


def manage_round(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    round_number = request.GET.get('round_number')

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
    header.add_cell(Cell('Penalty'))
    header.add_cell(Cell(''))
    header.add_cell(Cell(''))
    header.add_cell(Cell(''))
    header.add_cell(Cell(''))
    header.add_cell(Cell(''))
    table.set_header(header)

    # Later loop on rounds and round groups
    for round_group in f3f_round.groups:
        round_group.compute_scores()
        for competitor in sorted(round_group.runs):
            row = Line(name=Cell(str(competitor.bib_number)))
            row.add_cell(Cell(str(round_group.group_number)))
            row.add_cell(Cell(competitor.pilot.to_string()))
            row.add_cell(Cell(round_group.run_value_as_string(competitor)))
            row.add_cell(Cell(str(round_group.run_score_as_string(competitor))))
            row.add_cell(Cell(str(round_group.get_penalty(competitor))))
            row.add_cell(Link('Refly', 'give_refly?event_id='+str(event_id)+'&round_number='+str(round_number)+
                              '&bib_number='+str(competitor.bib_number)))
            row.add_cell(Link('Give 0', 'give_zero?event_id=' + str(event_id) + '&round_number=' + str(round_number) +
                              '&bib_number=' + str(competitor.bib_number)))
            row.add_cell(Link('Give 100 penalty', 'give_penalty?event_id=' + str(event_id) + '&round_number=' + str(round_number) +
                              '&bib_number=' + str(competitor.bib_number)+'&penalty=100'))
            row.add_cell(Link('Give 1000 penalty', 'give_penalty?event_id=' + str(event_id) + '&round_number=' + str(round_number) +
                              '&bib_number=' + str(competitor.bib_number)+'&penalty=1000'))
            row.add_cell(Link('Cancel penalty', 'give_penalty?event_id=' + str(event_id) + '&round_number=' + str(round_number) +
                              '&bib_number=' + str(competitor.bib_number)+'&penalty=0'))
            table.add_line(row)

    page.add_table(table)

    table = ResultTable(title='Flight order', css_id='ranking')
    header = Header(name=Cell('Bib'))
    header.add_cell(Cell('Group'))
    header.add_cell(Cell('Name'))
    header.add_cell(Cell(''))
    table.set_header(header)

    for group in f3f_round.groups:
        for bib_number in group.get_flight_order():
            row = Line(name=Cell(str(bib_number)))
            row.add_cell(Cell(str(group.group_number)))
            row.add_cell(Cell(f3f_round.event.competitors[bib_number].display_name()))
            row.add_cell(Link('Set time', 'set_time?event_id=' + str(event_id) + '&round_number=' + str(round_number) +
                              '&bib_number=' + str(bib_number)))
            table.add_line(row)

    page.add_table(table)

    result = page.to_html()
    return HttpResponse(result)


def give_refly(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    round_number = request.GET.get('round_number')
    bib_number = request.GET.get('bib_number')

    event = EventDAO().get(event_id, fetch_competitors=True)

    f3f_round = RoundDAO().get_from_ids(event.id, round_number, fetch_runs=True)

    competitor = event.competitors[int(bib_number)]

    f3f_run = f3f_round.get_valid_run(competitor)

    if f3f_run is not None:
        #If there is no valid flight, just add the pilot in the waiting list
        f3f_run.valid = False

    f3f_round.give_refly(competitor)

    return HttpResponseRedirect('manage_round?event_id='+event_id+'&round_number='+round_number)


def give_zero(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    round_number = request.GET.get('round_number')
    bib_number = request.GET.get('bib_number')

    event = EventDAO().get(event_id, fetch_competitors=True)

    f3f_round = RoundDAO().get_from_ids(event.id, round_number, fetch_runs=True)

    competitor = event.competitors[int(bib_number)]

    f3f_run = f3f_round.get_valid_run(competitor)

    f3f_run.valid = False

    RoundDAO().update(f3f_round)

    return HttpResponseRedirect('manage_round?event_id='+event_id+'&round_number='+round_number)


def give_penalty(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    round_number = request.GET.get('round_number')
    bib_number = request.GET.get('bib_number')
    penalty = int(request.GET.get('penalty'))

    event = EventDAO().get(event_id, fetch_competitors=True)

    f3f_round = RoundDAO().get_from_ids(event.id, round_number, fetch_runs=True)

    competitor = event.competitors[int(bib_number)]

    f3f_round.give_penalty(competitor, penalty)

    RoundDAO().update(f3f_round)

    return HttpResponseRedirect('manage_round?event_id='+event_id+'&round_number='+round_number)


def download_csv(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    round_number = request.GET.get('round_number')


    #We must fetch full event to get correct valid round number
    event = EventDAO().get(event_id, fetch_competitors=True, fetch_rounds=True, fetch_runs=True)
    requested_f3f_round = None
    for f3f_round in event.rounds:
        if f3f_round.round_number == int(round_number):
            requested_f3f_round = f3f_round

    if requested_f3f_round is not None:
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="round'+\
                                          str(requested_f3f_round.valid_round_number)+'.csv"'

        csv_writer = csv.writer(response)

        requested_f3f_round.export_to_csv(csv_writer)

        return response
    else:
        return HttpResponse('Round not found')


def download_pilots_as_csv(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')

    event = EventDAO().get(event_id, fetch_competitors=True, fetch_rounds=False, fetch_runs=False)

    if event is not None:
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="'+\
                                          str(event.name)+'.csv"'

        csv_writer = csv.writer(response)

        event.export_bibs_as_csv(csv_writer)

        return response
    else:
        return HttpResponse('Event not found')


def set_competitor_presence(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    bib_number = request.GET.get('bib_number')
    present = bool(int(request.GET.get('present')))

    event = EventDAO().get(event_id)

    dao = CompetitorDAO()

    competitor = dao.get(event, bib_number)

    competitor.present = present

    dao.update(competitor)

    return HttpResponseRedirect('manage_event?event_id='+event_id)


def remove_competitor(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    event_id = request.GET.get('event_id')
    bib_number = request.GET.get('bib_number')

    event = EventDAO().get(event_id, fetch_competitors=True)

    dao = CompetitorDAO()
    competitor = dao.get(event, bib_number)

    event.unregister_competitor(competitor, insert_database=True)

    return HttpResponseRedirect('manage_event?event_id='+event_id)

@never_cache
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('sign_in', request.path))

    Utils.set_port_number(request.META['SERVER_PORT'])

    dao = EventDAO()

    events = dao.get_list()

    page = ResultPage(title='F3F RACE MNGT Administration', authenticated=request.user.is_authenticated)

    table = ResultTable(title='', css_id='ranking')

    header = Header(name=Link('Create new event', 'create_new_event'))
    table.set_header(header)

    page.add_table(table)

    table = ResultTable(title='Manage existing event', css_id='ranking')

    header = Header(name=Cell('Event Name'))
    table.set_header(header)

    for event in events:
        fetched_event = dao.get(event.id)
        row = Line(name=Link(fetched_event.name, 'manage_event?event_id=' + str(fetched_event.id)))
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

