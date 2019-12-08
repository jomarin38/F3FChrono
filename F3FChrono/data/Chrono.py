

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

    def to_string(self):
        return str(self.run_time)

