def merge_lists(control_shift_list: list, guard_shift_list: list) -> list:
    """
    Merge together two shift lists from Control and guard type.
    Order is determine by date and time, control shift prior.
    :param control_shift_list: list of control shift.
    :param guard_shift_list: list of guard shift.
    :return: sorted list of shift in chronological order.
    """

    # pointer for control list
    control_pointer = 0
    # pointer for shift list
    guard_pointer = 0

    join_list = []

    while control_pointer < len(control_shift_list) and guard_pointer < len(guard_shift_list):

        # compare times
        if control_shift_list[control_pointer].time_range.start <= guard_shift_list[guard_pointer].time_range.start:
            join_list.append(control_shift_list[control_pointer])
            control_pointer += 1

        else:
            join_list.append(guard_shift_list[guard_pointer])
            guard_pointer += 1

        # if one of the pointers has reach the end, break the loop and continue it solo
        if control_pointer == len(control_shift_list) or guard_pointer == len(guard_shift_list):
            break

    # solo loop
    while control_pointer < len(control_shift_list):
        join_list.append(control_shift_list[control_pointer])
        control_pointer += 1

    while guard_pointer < len(guard_shift_list):
        join_list.append(guard_shift_list[guard_pointer])
        guard_pointer += 1

    return join_list


def split_lists(shift_list: list, start_shift: int):
    """
    Remove back count shifts from shift list and then, split shift list by type.
    :param shift_list: Completed shift list.
    :param start_shift: Remove shifts until this index.
    :return: two separated shift list, separated by type.
    """
    control_shift_list = []
    guard_shift_list = []

    # remove back_counting_shift_list from shift_list
    for index in range(start_shift):
        shift_list.pop(0)

    for shift in shift_list:

        # separate by type
        if shift.shift_type == "Control":
            control_shift_list.append(shift)

        if shift.shift_type == "Guard":
            guard_shift_list.append(shift)

    return control_shift_list, guard_shift_list
