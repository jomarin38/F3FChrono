from F3FChrono.data.Event import Event
from F3FChrono.data.dao.EventDAO import EventDAO
from F3FChrono.data.dao.CompetitorDAO import CompetitorDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO

login = input('F3X Vault login : ')
password = input('F3X Vault password : ')
contest_id = 1706

event = Event.from_f3x_vault(login, password, contest_id)

dao = EventDAO()

dao.insert(event)

event2 = dao.get_list()[-1]
event.id = event2.id

dao = CompetitorDAO()

for bib, competitor in event.get_competitors().items():
    dao.insert(competitor)

dao = RoundDAO()

for f3f_round in event.rounds:
    dao.insert(f3f_round)

print('Import finished')
