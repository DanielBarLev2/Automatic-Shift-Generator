from ..Classes.TimeRange import TimeRange
from ..Classes.Person import Person


class Shift:
    def __init__(self, time_range: TimeRange, person: Person, shift_type: str):
        self.time_range = time_range
        self.person = person
        self.shift_type = shift_type

    def get_duration_difference(self, other):
        """
        calculate duration in hours between self shift and other shift.
        - Self must be later than the other.
        :param other: former shift
        :return: the difference in hours between self shift and other shift
        """

        return abs(self.time_range.start - other.time_range.end)

    def __repr__(self):
        return f'{self.person} | - | {self.time_range} |  | {self.shift_type} '
