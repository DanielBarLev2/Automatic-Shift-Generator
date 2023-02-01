def is_complete(shift_list):
    """
    tests if shift list is completed and can be return.
    :param: shift_list: list of shifts
    :return: True if all shifts' person is not None. False otherwise.
    """

    for shift in shift_list:
        if shift.person is None:
            return False
    return True
