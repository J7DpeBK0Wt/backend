import json
from stats_mapper import make_stats_mapper


class StatsStore:
    def __init__(self, file_path, periods):
        self.stats = {}
        self.parse(file_path, periods)

    def parse(self, file_path, periods):
        with open(file_path) as json_file:
            mapper = make_stats_mapper(periods)
            self.stats = mapper.apply(json.load(json_file))

    def get_period(self, period):
        return self.stats.get(period)
