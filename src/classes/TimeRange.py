class TimeRange(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.duration = self.end - self.start

    def is_overlapped(self, time_range):
        return max(self.start, time_range.start) < min(self.end, time_range.end)

    def __repr__(self):
        return f' {self.start} - {self.end}'
