import os
from F3FChrono.data.dao.RunDAO import RunDAO
import sys

class RoundGroup:
    rundao=RunDAO()

    def __init__(self, f3f_round, group_number):
        self.round = f3f_round
        self.valid = False
        self.start_time = None
        self.end_time = None
        self.group_number = group_number
        self.runs = {}

    def add_run(self, run, insert_database=False):
        if run.competitor in self.runs:
            self.runs[run.competitor].append(run)
        else:
            self.runs[run.competitor] = [run]
        if (insert_database):
            RoundGroup.rundao.insert(run)
        #Set current competitor
        self.round.set_current_competitor(run.competitor)

    def get_valid_run(self, competitor):
        if competitor in self.runs:
            for run in self.runs[competitor]:
                if run.valid:
                    return run
        return None

    def has_run(self):
        return len(self.runs)>0

    def has_run_competitor(self, competitor):
        if competitor in self.runs:
            return len(self.runs[competitor]) > 0
        else:
            return False

    def get_penalty(self, competitor):
        penalty = 0
        if competitor in self.runs:
            for run in self.runs[competitor]:
                penalty += run.penalty
        return penalty

    def to_string(self):
        result = ''
        for competitor in sorted(self.runs):
            result += competitor.to_string() + '\t' + self.run_value_as_string(competitor) + os.linesep + os.linesep
        return result

    def run_value_as_string(self, competitor):
        valid_run = self.get_valid_run(competitor)
        if valid_run is not None and valid_run.chrono.run_time is not None:
            return '{:6.2f}'.format(valid_run.chrono.run_time)
        else:
            return 'Flight not valid'

    def run_score_as_string(self, competitor):
        valid_run = self.get_valid_run(competitor)
        if valid_run is not None:
            return str(valid_run.score_as_string())
        else:
            return str(0.0)

    def compute_scores(self):
        if self.has_run():
            run_times = [self.get_valid_run(competitor).get_flight_time() for competitor in sorted(self.runs)
                                 if self.get_valid_run(competitor) and self.get_valid_run(competitor).get_flight_time()]
            if len(run_times) > 0:
                best_run_time = min(run_times)
            else:
                best_run_time = 0
            for competitor in sorted(self.runs):
                valid_run = self.get_valid_run(competitor)
                if valid_run is not None:
                    if not valid_run.get_flight_time():
                        valid_run.score = 0.0
                    else:
                        valid_run.score = best_run_time / valid_run.get_flight_time() * 1000.0

    def get_best_run(self):
        best_run = None
        for competitor, runs in self.runs.items():
            for run in runs:
                if run.valid and (best_run is None or
                                  best_run.get_flight_time() is None or
                                  run.get_flight_time() < best_run.get_flight_time()):
                    best_run = run
        return best_run
