from src.algorithms.verify import is_valid_personnel_names, is_valid_time_range
from src.excel.read_data import create_shift_list, back_counting_shift_list, find_limits
from src.list_aid.merge_and_split import merge_lists, split_lists
from src.excel.availability import create_availability_schedule
from src.personnel.personnel import create_personnel_list
from src.excel.write_data import write_shift_list
from src.constants.columns import Columns
from src.algorithms.yael import yael
from src.screen.massage_box import *
from openpyxl import load_workbook


def load_and_divide_workbook() -> tuple:
    """
    Loads excel workbook and divides to sheets.
    :return: Shift, personnel and config worksheets. In addition, workbook.
    """
    while True:
        try:
            workbook = load_workbook(filename=Columns.FILE_NAME.value)

            # divides to sheets
            worksheet_shift = workbook[Columns.SHIFT_SHEET_NAME.value]
            worksheet_personnel = workbook[Columns.PERSONNEL_SHEET_NAME.value]

            return worksheet_shift, worksheet_personnel, workbook

        except PermissionError:
            answer = send_open_file_error()
            if answer == "cancel":
                return None, None, None

        except FileNotFoundError:
            answer = send_file_not_found_error(Columns.FILE_NAME.value)
            if answer == "cancel":
                return None, None, None


def create_personnel(worksheet_personnel, worksheet_shift, date_start_row: int, date_end_row: int) -> (list, list):
    # Creates a list with Person class object
    personnel_list = create_personnel_list(ws=worksheet_personnel)

    # create availability schedule for each person
    personnel_list, invalid_name_list = create_availability_schedule(ws=worksheet_shift, personnel_list=personnel_list,
                                                                     date_start_row=date_start_row,
                                                                     date_end_row=date_end_row)

    return personnel_list, invalid_name_list


def create_shift(worksheet_shift, start_row: int, end_row: int, past_days: int) -> (list, int):
    """
    Creates a shift list from the past and new shifts to be inserted.
    :return: list of shift from the past and new shifts to be inserted.
    """
    shift_list = back_counting_shift_list(worksheet=worksheet_shift, start_row=start_row, days=past_days)

    # set pointer to the first empty new shift
    start_shift = len(shift_list)

    # create shift list for control shifts
    control_shift_list = create_shift_list(worksheet=worksheet_shift, start_row=start_row, end_row=end_row,
                                           time_col=Columns.CONTROL_TIME.value)

    # create shift list for guard shifts
    guard_shift_list = create_shift_list(worksheet=worksheet_shift, start_row=start_row, end_row=end_row,
                                         time_col=Columns.GUARD_TIME.value)

    # merge past shift list with control shift list and guard shift list
    shift_list += merge_lists(control_shift_list=control_shift_list, guard_shift_list=guard_shift_list)

    return shift_list, start_shift


def write_and_save_workbook(worksheet_shift, control_shift_list: list, guard_shift_list: list, start_row: int,
                            end_row: int):
    """
    Writes to control shifts column and guard shifts column.
    :param worksheet_shift: excel shift list.
    :param control_shift_list: list of control shifts.
    :param guard_shift_list: list of guard shifts.
    :param start_row: start write row.
    :param end_row: end write row.
    """

    # write to control shift column
    write_shift_list(worksheet_shift, shift_list=control_shift_list, start_row=start_row, end_row=end_row,
                     person_col=Columns.CONTROL_PERSON.value)

    # write guard shift column
    write_shift_list(worksheet_shift, shift_list=guard_shift_list, start_row=start_row, end_row=end_row,
                     person_col=Columns.GUARD_PERSON.value)


def netta(start_date, end_date, past_days):
    """
    calls all the functions
    """

    error_massage = is_valid_time_range(start_date, end_date, past_days)

    if error_massage:
        send_time_set_error(is_valid_time_range(start_date, end_date, past_days))

    else:
        ws_shift, ws_personnel, workbook = load_and_divide_workbook()

        if not (ws_shift and ws_personnel and workbook):
            send_file_not_found_error(Columns.FILE_NAME.value)

        else:
            start_row, end_row, date_start_row, date_end_row = find_limits(ws=ws_shift,
                                                                           start_date_and_time=start_date,
                                                                           end_date_and_time=end_date)

            personnel_list, invalid_name_list = create_personnel(worksheet_personnel=ws_personnel,
                                                                 worksheet_shift=ws_shift,
                                                                 date_start_row=date_start_row,
                                                                 date_end_row=date_end_row)

            if send_not_enough_personnel_warning(personnel_list):

                if send_invalid_availability_name_error(invalid_name_list):

                    shift_list, start_shift = create_shift(worksheet_shift=ws_shift,
                                                           start_row=start_row,
                                                           end_row=end_row,
                                                           past_days=past_days)

                    invalid_name_list = is_valid_personnel_names(shift_list, personnel_list)

                    if send_invalid_person_name_error(invalid_name_list):

                        if send_not_complete_past_error(shift_list, start_shift):

                            shift_list = yael(shift_list, start_shift, personnel_list)

                            control_shift_list, guard_shift_list = split_lists(shift_list=shift_list,
                                                                               start_shift=start_shift)

                            write_and_save_workbook(worksheet_shift=ws_shift,
                                                    control_shift_list=control_shift_list,
                                                    guard_shift_list=guard_shift_list,
                                                    start_row=start_row,
                                                    end_row=end_row)

                            if send_failed_massage(shift_list):
                                workbook.save(filename=Columns.FILE_NAME.value)

                                send_end_massage()
