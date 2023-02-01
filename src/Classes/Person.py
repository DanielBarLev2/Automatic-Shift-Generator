class Person:
    def __init__(self, name: str, control_support: bool, guard_support: bool):
        self.name = name
        self.control_hours = 0
        self.guard_hours = 0
        self.control_support = control_support
        self.guard_support = guard_support
        self.former_gap = None
        self.latter_gap = None
        self.availability_schedule = []

    def is_available(self, shift) -> bool:
        """
        test if this person can be inserted to shift according to his availability schedule.
        :param shift: shift to insert person to.
        :return: True if the person can be inserted to shift. otherwise, return False.
        """
        # tests if person can support the current shift
        if (shift.shift_type == "Control" and self.control_support is True) or (shift.shift_type == "Guard" and
                                                                                self.guard_support is True):
            # the matrix is empty - the
            if not self.availability_schedule:
                return True
            else:
                for period in self.availability_schedule:
                    if shift.time_range.is_overlapped(period):
                        return False

            # all the periods have been confirmed
            return True

        else:
            return False

    def __repr__(self):
        return f'{self.name} | CH: {self.control_hours} | GH: {self.guard_hours} | {self.control_support} | ' \
               f'{self.guard_support} | FG: {self.former_gap} | LG: {self.latter_gap} '
