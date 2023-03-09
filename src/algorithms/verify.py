from src.constants.columns import Columns
from datetime import datetime


def is_valid_personnel_names(shift_list, personnel_list) -> list:
    """
    finds all the shift that has been assigned with wrong person name.
    (person's name is not existing in personnel list)
    :param shift_list: shift list.
    :param personnel_list: personnel list.
    :return: return the
    """

    invalid_shift_list = []

    for shift in shift_list:
        valid_name = False
        for person in personnel_list:
            if shift.person == person.name or not shift.person or shift.person == "x" or shift.person == "X":
                valid_name = True

        if not valid_name:
            invalid_shift_list.append(shift)

    return invalid_shift_list


def is_valid_availability_name(ws, personnel_list, row, time_range) -> (list, bool):
    """

    :param ws: shift worksheet.
    :param personnel_list: personnel list.
    :param row: row of the current person's name of availability column.
    :param time_range: the time range the person is not available at.
    :return: personnel_list and the misspelled person's name if accrued. If person exists, return None
    """
    person_name = ws.cell(column=Columns.ATTENDANCE.value, row=row).value

    for index, person in enumerate(personnel_list):
        if person_name == person.name:
            personnel_list[index].availability_schedule.append(time_range)
            return personnel_list, None

    return personnel_list, person_name


def is_valid_time_range(start_date, end_date, past_days):
    today = datetime.today()

    if today > start_date or today > end_date:
        return "Start date or end date cannot be set in the past"

    if past_days == 7 or abs(end_date - start_date).days > 7:
        return "Cannot exceed 7 days of generation"

    if start_date > end_date:
        return "Start date cannot be set after end date"

    return "No errors"
