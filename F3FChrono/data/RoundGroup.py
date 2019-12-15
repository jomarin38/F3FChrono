import os


class RoundGroup:

    def __init__(self, f3f_round, group_number):
        self.round = f3f_round
        self.valid = False
        self.start_time = None
        self.end_time = None
        self.group_number = group_number
        self.runs = {}

    def add_run(self, run):
        if run.competitor in self.runs:
            self.runs[run.competitor].append(run)
        else:
            self.runs[run.competitor] = [run]
        #Set current competitor
        self.round.set_current_competitor(run.competitor)

    def get_valid_run(self, competitor):
        if competitor in self.runs:
            for run in self.runs[competitor]:
                if run.valid:
                    return run

    def to_string(self):
        result = ''
        for competitor in sorted(self.runs):
            valid_run = self.get_valid_run(competitor)
            if (valid_run is not None):
                result += self.get_valid_run(competitor).to_string() + os.linesep
            else:
                result += competitor.to_string() + '\tFlight not valid' + os.linesep
        return result
