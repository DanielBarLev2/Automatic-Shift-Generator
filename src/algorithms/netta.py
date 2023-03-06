from src.algorithms.verify import is_valid_personnel_names, is_valid_time_range
from src.excel.read_data import create_shift_list, back_counting_shift_list, find_limits
from src.list_aid.Merge_and_Split import merge_lists, split_lists
from src.excel.Availability import create_availability_schedule
from src.personnel.Personnel import create_personnel_list
from src.excel.write_data import write_shift_list
from src.constants.Columns import Columns
from src.algorithms.yael import yael
from src.screen.massage_box import *
from openpyxl import load_workbook
from datetime import datetime


def load_and_divide_workbook():
    """
    Loads excel workbook and divides to sheets.
    :return: Shift, personnel and config worksheets. In addition, workbook.
    """

    while True:
        try:
            wb = load_workbook(filename=Columns.FILE_NAME.value)

            # divides to sheets
            ws_shift = wb[Columns.SHIFT_SHEET_NAME.value]
            ws_personnel = wb[Columns.PERSONNEL_SHEET_NAME.value]

            return ws_shift, ws_personnel, wb

        except PermissionError:
            answer = send_open_file_error()
            if answer == "cancel":
                return None, None, None

        except FileNotFoundError:
            answer = send_file_not_found_error(Columns.FILE_NAME.value)
            if answer == "cancel":
                return None, None, None


def create_personnel(ws_personnel, ws_shift, date_start_row: int, date_end_row: int) -> (list, list):
    # Creates a list with Person class object
    personnel_list = create_personnel_list(ws=ws_personnel)

    # create availability schedule for each person
    personnel_list, invalid_name_list = create_availability_schedule(ws=ws_shift, personnel_list=personnel_list,
                                                                     date_start_row=date_start_row,
                                                                     date_end_row=date_end_row)

    return personnel_list, invalid_name_list


def create_shift(ws_shift, start_row: int, end_row: int, past_days: int) -> (list, int):
    """
    Creates a shift list from the past and new shifts to be inserted.
    :return: list of shift from the past and new shifts to be inserted.
    """
    shift_list = back_counting_shift_list(worksheet=ws_shift, start_row=start_row, days=past_days)

    # set pointer to the first empty new shift
    start_shift = len(shift_list)

    # create shift list for control shifts
    control_shift_list = create_shift_list(ws=ws_shift, start_row=start_row, end_row=end_row,
                                           time_col=Columns.CONTROL_TIME.value)

    # create shift list for guard shifts
    guard_shift_list = create_shift_list(ws=ws_shift, start_row=start_row, end_row=end_row,
                                         time_col=Columns.GUARD_TIME.value)

    # join past shift list with control shift list and guard shift list
    shift_list += merge_lists(control_shift_list=control_shift_list, guard_shift_list=guard_shift_list)

    return shift_list, start_shift


def write_and_save_workbook(ws_shift, control_shift_list: list, guard_shift_list: list, start_row: int,
                            end_row: int):
    """
    Writes to control shifts column and guard shifts column.
    :param ws_shift: excel shift list.
    :param control_shift_list: list of control shifts.
    :param guard_shift_list: list of guard shifts.
    :param start_row: start write row.
    :param end_row: end write row.
    """

    # write to control shift column
    write_shift_list(ws_shift, shift_list=control_shift_list, start_row=start_row, end_row=end_row,
                     person_col=Columns.CONTROL_PERSON.value)

    # write guard shift column
    write_shift_list(ws_shift, shift_list=guard_shift_list, start_row=start_row, end_row=end_row,
                     person_col=Columns.GUARD_PERSON.value)


def netta(start_date, end_date, past_days):
    """
    calls all the functions
    """

    load_time = datetime.now()

    valid_setup = is_valid_time_range(start_date, end_date, past_days)

    if send_time_set_error(valid_setup):

        ws_shift, ws_personnel, workbook = load_and_divide_workbook()

        if ws_shift and ws_personnel and workbook:

            start_row, end_row, date_start_row, date_end_row = \
                find_limits(ws=ws_shift, start_date_and_time=start_date, end_date_and_time=end_date)

            personnel_list, invalid_name_list = create_personnel(ws_personnel=ws_personnel, ws_shift=ws_shift,
                                                                 date_start_row=date_start_row,
                                                                 date_end_row=date_end_row)

            if send_not_enough_personnel_warning(personnel_list):

                if send_invalid_availability_name_error(invalid_name_list):

                    shift_list, start_shift = create_shift(ws_shift=ws_shift, start_row=start_row,
                                                           end_row=end_row, past_days=past_days)

                    invalid_name_list = is_valid_personnel_names(shift_list, personnel_list)

                    if send_invalid_person_name_error(invalid_name_list):
                        shift_list = yael(shift_list, start_shift, personnel_list)

                        control_shift_list, guard_shift_list = split_lists(shift_list=shift_list,
                                                                           start_shift=start_shift)

                        write_and_save_workbook(ws_shift=ws_shift, control_shift_list=control_shift_list,
                                                guard_shift_list=guard_shift_list, start_row=start_row, end_row=end_row)

                        if send_failed_massage(shift_list):

                            workbook.save(filename=Columns.FILE_NAME.value)

                            send_end_massage(load_time)
