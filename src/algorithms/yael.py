from src.algorithms.placement import sort_by_placement, is_valid_placement
from src.list_aid.Complete import is_complete
from src.personnel.Rank import update_rank


def yael(shift_list, start_shift, personnel_list) -> list:
    """
    The function is recurring.
    It uses Back Tracking to avoid and prevent impossible placements, by trying all the possible combination.
    1. Run through all shifts in shift list, finds the empty shifts.
    2. Sort the personnel list by gaps between former and latter shifts.
    3. Tries to place a person by testing availability schedule and valid placements.
    4. Place the person and add the duration to rank values.
    5. If there are no more valid placements, jump back to the former shift, and reset its placement.
    6. If the shift list is filled with valid personnel, return complete shift list.
    :param shift_list: empty shift list.
    :param start_shift: the first empty shift index.
    :param personnel_list: personnel list.
    :return: a completed shift list, filled with personnel from personnel list.
    """

    # iterate through shift list
    for shift in shift_list[start_shift:]:

        # finds the next empty shift
        if shift.person is None:

            # sort the personnel list by former_gap, then by latter_gap
            personnel_list = sort_by_placement(shift_list, personnel_list, shift)

            # tries to insert each personnel by validation
            for person in personnel_list:

                # Tries to place a person by testing availability schedule and valid placements.
                if person.is_available(shift) and is_valid_placement(shift_list, person, shift):

                    # insert person to shift
                    shift.person = person.name

                    # update rank matrix by summation
                    personnel_list = update_rank(personnel_list, person.name, shift.time_range.duration,
                                                 shift.shift_type)

                    # continue to next shift by recursion
                    shift_list = yael(shift_list, start_shift, personnel_list)

                    if is_complete(shift_list):
                        # the process is completed
                        return shift_list
                    else:
                        # wrong person was inserted to shift, tries next
                        shift.person = None

                    # updating rank matrix by subtraction
                    personnel_list = update_rank(personnel_list, person.name, shift.time_range.duration,
                                                 shift.shift_type)
            return shift_list

    return shift_list
