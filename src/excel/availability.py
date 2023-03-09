from src.algorithms.verify import is_valid_availability_name
from datetime import time, datetime, timedelta
from src.classes.TimeRange import TimeRange
from src.constants.columns import Columns


def create_availability_schedule(ws, personnel_list: list, date_start_row: int, date_end_row: int) -> (list, list):
    """
    creates a schedule for each person. contains the periods which the person is not present.
    the purpose is to valid that the person is available when he needs to be used.
    the function reads data from ATTENDANCE, DEPARTURE, ARRIVAL columns and insert them to the appropriate personnel
    member.
    :param ws: excel worksheet
    :param personnel_list: list with workers' names and hours in shifts
    :param date_start_row: date to begin the list
    :param date_end_row: date to end the list
    :return: matrix containing name and all the ranges, in date_to_date format, the worker is not present
    """

    # bounds
    row = date_start_row + 1
    end_row = date_end_row + Columns.DATE_CELL_SIZE.value

    invalid_name_list = []

    while row < end_row or ws.cell(column=Columns.ATTENDANCE.value, row=row).value is not None:

        # update the current date when needed
        if ws.cell(column=Columns.DATE.value, row=row).value is not None:
            date_start_row = row

        if ws.cell(column=Columns.ATTENDANCE.value, row=row).value is not None:
            # get values from column respectively
            start_date = ws.cell(column=Columns.DATE.value, row=date_start_row).value.date()
            departure = ws.cell(column=Columns.DEPARTURE.value, row=row).value
            arrival = ws.cell(column=Columns.ARRIVAL.value, row=row).value

            # avoid empty entries and wrong inputs
            if isinstance(departure, datetime):
                departure = departure.time()

            if isinstance(arrival, datetime):
                arrival = arrival.time()

            if isinstance(departure, time) and isinstance(arrival, time):

                start_datetime = datetime.combine(start_date, departure)

                if arrival == time(0, 0, 0):
                    end_date = start_date + timedelta(days=1)
                    end_datetime = datetime.combine(end_date, arrival)
                else:
                    end_datetime = datetime.combine(start_date, arrival)

                # store the values in an instance of date to date object
                time_range = TimeRange(start_datetime, end_datetime)

                personnel_list, invalid_person = is_valid_availability_name(ws, personnel_list, row, time_range)

                if invalid_person:
                    invalid_name_list.append(invalid_person)

        row += 1

    return personnel_list, invalid_name_list
