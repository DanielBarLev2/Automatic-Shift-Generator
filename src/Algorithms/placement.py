from ..Classes.Person import Person
from ..Enum.Columns import Columns
from ..Classes.Shift import Shift
from datetime import timedelta


def find_former_current_latter_index(shift_list: list, shift: Shift, person: Person) -> tuple:
    """
    Finds person's current shift placement and his former and latter shift placements, if they are existed.
    :param shift_list: incomplete shift list.
    :param shift: current shift placement.
    :param person: person to place.
    :return: former latter and current index placements for person's shifts.
    """

    # shifts' indexes
    current_shift = 0
    former_shift = None
    latter_shift = None

    # finds former shift's and current shift's index
    while shift_list[current_shift] != shift:

        # update former shift index
        if shift_list[current_shift].person == person.name:
            former_shift = current_shift

        current_shift += 1

    temp_index = current_shift

    # continue the loop, finds the latter shift's index
    while temp_index < len(shift_list):

        # update latter shift index
        if shift_list[temp_index].person == person.name:
            latter_shift = temp_index
            # exits the while loop
            break

        temp_index += 1

    return former_shift, current_shift, latter_shift


def sort_by_placement(shift_list: list, personnel_list: list, shift: Shift) -> list:
    """
    Calculates how many hours have passed since person's last shift and how many hours will pass until next shift.
    then, insert them into person's former_shift and latter_shift values.
    - If there are no shift placements before or after, insert min or max datetime respectively.
    :param shift_list: list of shifts.
    :param shift: current shift placement.
    :param personnel_list: list of persons.
    :return: sorted personnel list by former_gap and latter_gap.
    """

    # scan personnel list
    for index, person in enumerate(personnel_list):
        former_shift, current_shift, latter_shift = find_former_current_latter_index(shift_list, shift, person)

        # calculate the gap between former shift and current shift
        if former_shift is None:
            former_gap = timedelta.max
        else:
            former_gap = shift_list[current_shift].get_duration_difference(shift_list[former_shift])

        # calculate the gap between latter shift and current shift
        if latter_shift is None:
            latter_gap = timedelta.max
        else:
            latter_gap = shift_list[latter_shift].get_duration_difference(shift_list[current_shift])

        # update the person gap values
        personnel_list[index].former_gap = former_gap
        personnel_list[index].latter_gap = latter_gap

    # sort the personnel list by former_gap, then by latter_gap
    personnel_list = sorted(personnel_list, key=lambda x: (x.former_gap, x.latter_gap), reverse=True)

    return personnel_list


def is_valid_placement(shift_list: list, person: Person, shift: Shift) -> bool:
    """
    Calculates how many hours have passed since person's last shift and how many hours will pass until next shift.
    then, compare them to max gap possible.
    :param shift_list: list of shifts.
    :param shift: current shift placement.
    :param person: list of persons.
    :return: return True if the gap between placements is wide enough. otherwise, return False.
    """

    # scan personnel list
    former_shift, current_shift, latter_shift = find_former_current_latter_index(shift_list, shift, person)

    # calculate the gap between former shift and current shift, and the gap between latter shift and current shift
    if former_shift is None:
        former_gap = timedelta.max
    else:
        former_gap = shift_list[current_shift].get_duration_difference(shift_list[former_shift])

    if latter_shift is None:
        latter_gap = timedelta.max
    else:
        latter_gap = shift_list[latter_shift].get_duration_difference(shift_list[current_shift])

    return Columns.MAX_GAP.value <= former_gap and Columns.MAX_GAP.value <= latter_gap
