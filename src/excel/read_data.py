from src.list_aid.merge_and_split import merge_lists
from datetime import time, datetime, timedelta
from src.classes.TimeRange import TimeRange
from src.constants.columns import Columns
from src.classes.Shift import Shift


def find_limits(ws, start_date_and_time: datetime, end_date_and_time: datetime) -> (int, int, int, int):
    """
    Finds the column pointing on the desired start date, then finds the desired start time.
    Next, finds the column pointing on the desired end date, then finds the desired end time.
    :param ws: Excel shift worksheet.
    :param start_date_and_time: The targeted start date.
    :param end_date_and_time: The targeted end date.
    :return: The start row and end row that contain start date time and end date time.
    """

    start_row = 1

    # finds starting date
    while start_row < Columns.MAX_ROW_LIMIT.value:
        cell = ws.cell(column=Columns.DATE.value, row=start_row).value
        if isinstance(cell, datetime):
            if cell.date() == start_date_and_time.date():
                break
        start_row += 1

    date_to_start = start_row

    # finds starting time
    while start_row < start_row + Columns.DATE_CELL_SIZE.value:
        cell = ws.cell(column=Columns.CONTROL_TIME.value, row=start_row).value
        if cell is not None:
            if str(start_date_and_time.time().hour) in \
                    str.split(cell)[0]:
                break
        start_row += 1

    end_row = start_row

    # finds ending date
    while end_row < Columns.MAX_ROW_LIMIT.value:
        cell = ws.cell(column=Columns.DATE.value, row=end_row).value
        if isinstance(cell, datetime):
            if cell.date() == end_date_and_time.date():
                break
        end_row += 1

    date_to_end = end_row

    # finds ending time
    while end_row < end_row + Columns.DATE_CELL_SIZE.value:
        if str(end_date_and_time.time().hour) in str(ws.cell(column=Columns.CONTROL_TIME.value, row=end_row).value):
            break
        start_row += 1

    return start_row, end_row, date_to_start, date_to_end


def create_shift_list(worksheet, start_row: int, end_row: int, time_col: int) -> list:
    """
    Creates a shift list from excel workbook from start row to end row.
    :param worksheet: excel shift worksheet.
    :param start_row: the first shift in the sheet
    :param end_row: the last shift in the sheet.
    :param time_col: the column that contains the time values stored at the sheet.
    :return: a list of shifts, ready to be inserted with workers.
    """

    shift_list = []

    while start_row <= end_row:
        cell = worksheet.cell(column=time_col, row=start_row)
        # Iterates through real cells and skips merged cells.
        if type(cell).__name__ == 'Cell':
            # find only empty cells
            if cell.value is not None\
                    and worksheet.cell(column=(time_col + 1), row=start_row).value != " ":

                # extracts start and end time from the workbook
                start_time = int(str.split(str.split(str(cell.value))[0], ":")[0])
                end_time = int(str.split(str.split(cell.value)[2], ":")[0])

                # distinguishes between shift types and insert person
                shift_type = None
                person = None

                if time_col == Columns.CONTROL_TIME.value:
                    shift_type = "Control"
                    person = worksheet.cell(column=Columns.CONTROL_PERSON.value, row=start_row).value

                elif time_col == Columns.GUARD_TIME.value:
                    shift_type = "Guard"
                    person = worksheet.cell(column=Columns.GUARD_PERSON.value, row=start_row).value

                # reads the current date from excel
                date_start_row = start_row
                while worksheet.cell(column=Columns.DATE.value, row=date_start_row).value is None:
                    date_start_row -= 1

                # update the date with respect to merged cells
                date = worksheet.cell(column=Columns.DATE.value, row=date_start_row).value.date()

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
