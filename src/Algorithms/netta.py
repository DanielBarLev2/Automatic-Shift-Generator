from src.Excel.read_data import create_shift_list, back_counting_shift_list, find_limits, get_start_and_end_time
from src.List_Aid.Merge_and_Split import merge_lists, split_lists
from src.Excel.Availability import create_availability_schedule
from src.Personnel.Personnel import create_personnel_list
from src.Excel.write_data import write_shift_list
from src.Algorithms.yael import yael
from src.Enum.Columns import Columns
from openpyxl import load_workbook
from tkinter import messagebox
from datetime import datetime
import tkinter as tk


def load_and_divide_workbook():
    """
    Loads excel workbook and divides to sheets.
    :return: Shift, Personnel and config worksheets. In addition, workbook.
    """

    wb = load_workbook(filename=Columns.FILE_NAME.value)

    # divides to sheets
    ws_shift = wb[Columns.SHIFT_SHEET_NAME.value]
    ws_personnel = wb[Columns.PERSONNEL_SHEET_NAME.value]
    ws_config = wb[Columns.CONFIG_SHEET_NAME.value]

    return ws_shift, ws_personnel, ws_config, wb


def create_personnel(ws_personnel, ws_shift, date_start_row: int, date_end_row: int) -> list:
    # Creates a list with Person class object
    personnel_list = create_personnel_list(ws=ws_personnel)

    # create availability schedule for each person
    personnel_list = create_availability_schedule(ws=ws_shift, personnel_list=personnel_list,
                                                  date_start_row=date_start_row, date_end_row=date_end_row)

    return personnel_list


def create_shift(ws_shift, start_row: int, end_row: int) -> (list, int):
    """
    Creates a shift list from the past and new shifts to be inserted.
    :return: list of shift from the past and new shifts to be inserted.
    """
    shift_list = back_counting_shift_list(worksheet=ws_shift, start_row=start_row, days=Columns.PAST_DAYS.value)

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


def write_and_save_workbook(wb, ws_shift, control_shift_list: list, guard_shift_list: list, start_row: int,
                            end_row: int):
    """
    Writes to control shifts column and guard shifts column.
    :param wb: workbook
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

    wb.save(filename=Columns.FILE_NAME.value)


def send_end_massage(shift_list: list, personnel_list: list, load_time: datetime):
    """

    :param shift_list: list of control shifts.
    :param personnel_list: list of personnel
    :param load_time: load time
    :return: send an end message
    """
    end_massage = ""
    end_massage += "--- Shifts: \n"

    for shift in shift_list:
        end_massage += f'{shift.time_range} in {shift.person} \n'

    end_massage += "--- Personnel: \n"
    for person in personnel_list:
        end_massage += f'{person} \n'
        for available in person.availability_schedule:
            end_massage += f'{available} \n'

    # end of script message box
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("End", f'Total Time: {datetime.now() - load_time}' + "\n" + end_massage)


def netta():
    """
    calls all the functions
    """

    # loads excel workbook and divides to sheets
    load_time = datetime.now()
    ws_shift, ws_personnel, ws_config, workbook = load_and_divide_workbook()
    print(f' end of load: {datetime.now() - load_time}')

    # reads start and end date time from config sheet
    start, end = get_start_and_end_time(ws=ws_config)

    # finds start row and end row in shift sheet. In addition, return the first row in the start date and end date
    start_row, end_row, date_start_row, date_end_row = \
        find_limits(ws=ws_shift, start_date_and_time=start, end_date_and_time=end)

    # read shifts from the past for future evaluation
    personnel_list = create_personnel(ws_personnel=ws_personnel, ws_shift=ws_shift, date_start_row=date_start_row,
                                      date_end_row=date_end_row)

    # Creates a shift list from the past and new shifts to be inserted.
    shift_list, start_shift = create_shift(ws_shift=ws_shift, start_row=start_row, end_row=end_row)

    # place shifts with respect for wide enough placements
    shift_list = yael(shift_list, start_shift, personnel_list)

    # separate the list
    control_shift_list, guard_shift_list = split_lists(shift_list=shift_list, start_shift=start_shift)

    print(f' end of algorithm: {datetime.now() - load_time}')

    # Writes to control shifts column and guard shifts column.
    write_and_save_workbook(wb=workbook, ws_shift=ws_shift, control_shift_list=control_shift_list,
                            guard_shift_list=guard_shift_list, start_row=start_row, end_row=end_row)

    send_end_massage(shift_list, personnel_list, load_time)
