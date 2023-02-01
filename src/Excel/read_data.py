from src.List_Aid.Merge_and_Split import merge_lists
from datetime import time, datetime, timedelta
from src.Classes.TimeRange import TimeRange
from src.Enum.Columns import Columns
from src.Classes.Shift import Shift


def get_start_and_end_time(ws):
    """
    Reads start and end date time from config sheet.
    :param ws: excel config worksheet.
    :return: start and end datetime.
    """
    start_date = ws[Columns.START_DATE.value].value
    end_date = ws[Columns.END_DATE.value].value
    start_time = ws[Columns.START_TIME.value].value
    end_time = ws[Columns.END_TIME.value].value

    start_date = datetime.combine(start_date, start_time)
    end_date = datetime.combine(end_date, end_time)

    return start_date, end_date


def find_limits(ws, start_date_and_time: datetime, end_date_and_time: datetime) -> (int, int, int, int):
    """
    Finds the column pointing on the desired start date, then finds the desired start time.
    Next, finds the column pointing on the desired end date, then finds the desired end time.
    :param ws: excel shift worksheet.
    :param start_date_and_time: the targeted start date.
    :param end_date_and_time: the targeted end date.
    :return: the start row and end row that containing start date time and end date time.
    """

    start_row = 1

    # finds starting date
    while start_row < Columns.MAX_ROW_LIMIT.value:
        if isinstance(ws.cell(column=Columns.DATE.value, row=start_row).value, datetime):
            if ws.cell(column=Columns.DATE.value, row=start_row).value.date() == start_date_and_time.date():
                break
        start_row += 1

    date_to_start = start_row

    # finds starting time
    while start_row < start_row + Columns.DATE_CELL_SIZE.value:
        if ws.cell(column=Columns.CONTROL_TIME.value, row=start_row).value is not None:
            if str(start_date_and_time.time().hour) in \
                    str.split(ws.cell(column=Columns.CONTROL_TIME.value, row=start_row).value)[0]:
                break
        start_row += 1

    end_row = start_row

    # finds ending date
    while end_row < Columns.MAX_ROW_LIMIT.value:
        if isinstance(ws.cell(column=Columns.DATE.value, row=end_row).value, datetime):
            if ws.cell(column=Columns.DATE.value, row=end_row).value.date() == end_date_and_time.date():
                break
        end_row += 1

    date_to_end = end_row

    # finds ending time
    while end_row < end_row + Columns.DATE_CELL_SIZE.value:
        if str(end_date_and_time.time().hour) in str(ws.cell(column=Columns.CONTROL_TIME.value, row=end_row).value):
            break
        start_row += 1

    return start_row, end_row, date_to_start, date_to_end


def create_shift_list(ws, start_row: int, end_row: int, time_col: int) -> list:
    """
    Creates a shift list from Excel workbook from start row to end row.
    :param ws: excel shift worksheet.
    :param start_row: the first shift in the sheet
    :param end_row: the last shift in the sheet.
    :param time_col: the column that contains the time values stored at the sheet.
    :return: a list of shifts, ready to be inserted with workers.
    """

    shift_list = []

    while start_row <= end_row:
        # Iterates through real cells and skips merged cells.
        if type(ws.cell(column=time_col, row=start_row)).__name__ == 'Cell':
            # find only empty cells
            if ws.cell(column=time_col, row=start_row).value is not None\
                    and ws.cell(column=(time_col + 1), row=start_row).value != " ":

                # extracts start and end time from the workbook
                start_time = int(str.split(str.split(str(ws.cell(column=time_col, row=start_row).value))[0], ":")[0])
                end_time = int(str.split(str.split(str(ws.cell(column=time_col, row=start_row).value))[2], ":")[0])

                # distinguishes between shift types and insert person
                shift_type = None
                person = None

                if time_col == Columns.CONTROL_TIME.value:
                    shift_type = "Control"
                    person = ws.cell(column=Columns.CONTROL_PERSON.value, row=start_row).value

                elif time_col == Columns.GUARD_TIME.value:
                    shift_type = "Guard"
                    person = ws.cell(column=Columns.GUARD_PERSON.value, row=start_row).value

                # reads the current date from excel
                date_start_row = start_row
                while ws.cell(column=Columns.DATE.value, row=date_start_row).value is None:
                    date_start_row -= 1

                # update the date with respect to merged cells
                date = ws.cell(column=Columns.DATE.value, row=date_start_row).value.date()

                start_datetime = datetime.combine(date, time(start_time, 0, 0))
                end_datetime = start_datetime

                # Shift does not exceed to nighttime:
                if Columns.DAY_START.value <= start_time and Columns.DAY_START.value < end_time < Columns.DAY_END.value:
                    end_datetime = datetime.combine(date, time(end_time, 0, 0))

                # Shift starts and ends after midnight
                elif Columns.NIGHT_START.value <= start_time < Columns.DAY_START.value:
                    start_datetime = datetime.combine(date, time(start_time, 0, 0)) + timedelta(days=1)
                    end_datetime = datetime.combine(date, time(end_time, 0, 0)) + timedelta(days=1)

                # Shift starts at daytime and exceeds to nighttime, increasing the end date only.
                elif end_time < Columns.DAY_START.value <= start_time:
                    end_datetime = datetime.combine(date, time(end_time, 0, 0)) + timedelta(days=1)

                shift_list.append(Shift(TimeRange(start_datetime, end_datetime), person, shift_type))

        start_row += 1

    return shift_list


def back_counting_shift_list(worksheet, start_row: int, days: int) -> list:
    """
    Creates a shift list from excel workbook, insert data from X days ago from the current date.
    The list contain both CONTROL and GUARD shift in order.
    The purpose: use past shift to determine prime order to personnel list
    :param days: how many days should be added to the back counting
    :param worksheet: excel shift worksheet
    :param start_row: countdown the hours from a respected range until this row
    :return: 24 hours ago shift list.
    """

    # create a shift list from last days
    control_shift_list = create_shift_list(worksheet, start_row - days * Columns.DATE_CELL_SIZE.value, start_row - 1,
                                           Columns.CONTROL_TIME.value)

    guard_shift_list = create_shift_list(worksheet, start_row - days * Columns.DATE_CELL_SIZE.value, start_row - 1,
                                         Columns.GUARD_TIME.value)

    shift_list = merge_lists(control_shift_list, guard_shift_list)

    return shift_list
