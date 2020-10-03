import datetime


class History:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.end_time = None

        self.total_rounds = 0
        self.max_success_level = 0
        self.levels = {}

        self.report = None

    def add_result(self, level, outcome):
        if level not in self.levels:
            self.levels[level] = {
                'success': 0,
                'fail': 0,
                'total': 0,
            }

        self.levels[level][outcome] += 1
        self.levels[level]['total'] += 1
        self.total_rounds += 1

        if outcome == 'success' and level > self.max_success_level:
            self.max_success_level = level

    def calculate_percentages(self):
        for level_stats in self.levels.values():
            level_stats['success_rate'] = round(
                (level_stats['success'] * 100) / level_stats['total'],
                2,
            )

    def generate_report(self):
        self.end_time = datetime.datetime.now()
        self.calculate_percentages()

        self.report = {
            'time': {
                'start': str(self.start_time),
                'end': str(self.end_time),
                'duration': str(self.end_time - self.start_time),
            },
            'total_rounds': self.total_rounds,
            'max_success_level': self.max_success_level,
            'levels': self.levels,
        }
