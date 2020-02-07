import os

class Chrono:

    def __init__(self):
        self.id = None
        self.run_time = None
        self.min_wind_speed = None
        self.max_wind_speed = None
        self.wind_direction = None
        self.start_time = None
        self.end_time = None
        self._lap_times = []

    def get_lap_time(self, i):
        if i < len(self._lap_times):
            return self._lap_times[i]
        else:
            return None

    def add_lap_time(self, lap_time):
        self._lap_times.append(lap_time)

    def reset(self):
        self.id = None
        self.run_time = None
        self.min_wind_speed = None
        self.max_wind_speed = None
        self.wind_direction = None
        self.start_time = None
        self.end_time = None
        self._lap_times.clear()

    def to_string(self):
        result=''
        if (self.run_time!=None):
            result = os.linesep + "Chrono Data : " + os.linesep +\
                     "\tStart Time : " + str(self.start_time) + os.linesep +\
                     "\tEnd Time : " + str(self.end_time) + os.linesep +\
                     "\tWindMin : "+str(self.min_wind_speed)+", WindMax : "+str(self.max_wind_speed)+", WindDir : "+"{:0>.2f}".format(self.wind_direction)+os.linesep+\
                     "\tRun Time : " + self.run_time_as_string() + os.linesep + "\tLapTime : "
            for lap in self._lap_times:
                if lap!=None:
                    result += "{:0>6.3f}".format(lap) + ","
            result += os.linesep
        return result

    def run_time_as_string(self):
        return "{:6.2f}".format(self.run_time)
