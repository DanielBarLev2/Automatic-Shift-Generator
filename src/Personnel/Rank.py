def update_rank(personnel_list: list, person_name: str, duration, shift_type: str) -> list:
    """
    INDIVIDUAL UPDATE - extract person name from shift and then add shift duration to Person according to shift type.
    :param shift_type: determines where to insert shift ranking: Control-1, Guard-2
    :param personnel_list:  list with workers' names and hours in shifts
    :param person_name: the person to increase his ranking
    :param duration: the duration of a shift - rank score
    :return: person with update shift rank
    """

    for person in personnel_list:
        if person_name == person.name:
            if shift_type == "Control":
                person.control_hours += duration.seconds // 3600
            else:
                person.guard_hours += duration.seconds // 3600

    return personnel_list


# def update_personnel_rank_list(personnel_list: list, past_shift_list: list) -> list:
#     """
#     COLLECTIVE UPDATE
#     insert shift duration to the proper personnel in personnel list.
#     uses a shift list and updates all rank values to personnel
#     :param personnel_list: update personnel working hours by shift list
#     :param past_shift_list: hours that have been worked by personnel before
#     :return: updated personnel list with past rank
#     """
#
#     # go through shift list
#     for shift in past_shift_list:
#         # find the person in personnel and insert duration
#         personnel_list = update_rank(personnel_list, shift.person, shift.time_range.duration,
#                                      shift.shift_type)
#
#     return personnel_list


# def initialise_personnel_list(personnel_list: list) -> list:
#     """
#     reset shifts' total duration value to zero.
#     the purpose: give priority to personnel that was used before
#     :param personnel_list: personnel list with updated shift duration from the past.
#     :return: initialised personnel list
#     """
#
#     # initialise with zero's
#     for person in personnel_list:
#         person.control_hours = 0
#         person.guard_hours = 0
#
#     return personnel_list
