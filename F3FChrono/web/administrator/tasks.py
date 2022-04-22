from celery import shared_task
from celery_progress.backend import ProgressRecorder

from F3FChrono.data.dao.EventDAO import EventDAO
from F3FChrono.data.Round import Round

@shared_task(bind=True)
def f3x_vault_export_task(self, event_id, round_number, f3x_username, f3x_password):
    progress_recorder = ProgressRecorder(self)

    # We must fetch full event to get correct valid round number
    event = EventDAO().get(event_id, fetch_competitors=True, fetch_rounds=True, fetch_runs=True)
    requested_f3f_round = None
    for f3f_round in event.rounds:
        if f3f_round.round_number == int(round_number):
            requested_f3f_round = f3f_round

    if requested_f3f_round is not None:
        requested_f3f_round.export_to_f3x_vault(f3x_username, f3x_password, progress_recorder)
    return 0
