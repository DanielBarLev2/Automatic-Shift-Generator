from datetime import datetime, timedelta
from src.Algorithms import netta
from tkinter import ttk
import tkinter as tk
import calendar

MONTH_LIST_NAME = ('January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December')

TIME_LIST_NAME = ("00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00",
                  "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                  "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00")

RESOLUTION = "500x400"
TITLE = "NETTA"
HEADER = "Yael's Auto-Shift-Generation"
ICON = 'Netta_Icon.ico'


def create_window(window):
    window.geometry(RESOLUTION)
    window.title(TITLE)

    # Center the window on the screen
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()

    position_right = int(window.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(window.winfo_screenheight() / 2 - window_height / 2)

    window.geometry("+{}+{}".format(position_right, position_down))

    # Set the window icon
    # window.iconbitmap(ICON)


def crate_labels(window):
    title_label = tk.Label(window, text=HEADER, font=("Arial", 16))
    title_label.grid(column=0, row=0, columnspan=5, pady=20, padx=40)

    from_label = tk.Label(window, text="From:")
    from_label.grid(column=0, row=1, pady=10, padx=10)

    to_label = tk.Label(window, text="To:")
    to_label.grid(column=0, row=2, pady=10, padx=10)

    to_label = tk.Label(window, text="Take")
    to_label.grid(column=0, row=3, pady=10, padx=10)

    to_label = tk.Label(window, text="days into account")
    to_label.grid(column=2, row=3, pady=10, padx=10)


def create_drop_down_list(window):
    account_drop_down = ttk.Combobox(window, values=tuple(range(0, 7)), width=8, justify="center")
    account_drop_down.grid(column=1, row=3, padx=10, pady=10)
    account_drop_down.current(2)

    return [account_drop_down]


def create_drop_down_list_for_date(window, row: str):
    # create drop down
    year_drop_down = ttk.Combobox(window, values=tuple(range(2020, 2030)), width=8, justify="center")
    month_drop_down = ttk.Combobox(window, values=MONTH_LIST_NAME, width=8, justify="center")
    day_drop_down = ttk.Combobox(window, values=tuple(range(1, 32)), width=8, justify="center")
    time_drop_down = ttk.Combobox(window, values=TIME_LIST_NAME, width=8, justify="center")

    if row == "from":
        row_in = 1
    else:
        row_in = 2

    # center
    year_drop_down.grid(column=4, row=row_in, padx=10, pady=10)
    month_drop_down.grid(column=3, row=row_in, padx=10, pady=10)
    day_drop_down.grid(column=2, row=row_in, padx=10, pady=10)
    time_drop_down.grid(column=1, row=row_in, padx=10, pady=10)

    return set_default_value_to_drop_down_list(year_drop_down, month_drop_down, day_drop_down, time_drop_down, row)


def set_default_value_to_drop_down_list(year_drop_down, month_drop_down, day_drop_down, time_drop_down, row):
    date = datetime.now()

    # respective to lists indexes
    from_year = date.year - 2020
    from_month = date.month - 1
    from_day = date.day

    # adapt the default time delta between 'from date' and 'to date'
    if calendar.day_name[date.weekday()] == 'Saturday':
        date = datetime.now()
        date += timedelta(days=5)

        to_year = date.year - 2020
        to_month = date.month - 1
        to_day = date.day - 1

    else:
        date = datetime.now()
        date += timedelta(days=3)

        to_year = date.year - 2020
        to_month = date.month - 1
        to_day = date.day - 1

    if row == "from":
        year_drop_down.current(from_year)
        month_drop_down.current(from_month)
        day_drop_down.current(from_day)
        time_drop_down.current(12)

    elif row == "to":
        year_drop_down.current(to_year)
        month_drop_down.current(to_month)
        day_drop_down.current(to_day)
        time_drop_down.current(12)

    return year_drop_down, month_drop_down, day_drop_down, time_drop_down


def unpack_and_send_data(drop_down_list):

    data = []
    for combo_bix in drop_down_list:
        # convert month names into strings
        if combo_bix.get() in MONTH_LIST_NAME:
            data.append(MONTH_LIST_NAME.index(combo_bix.get()) + 1)

        elif combo_bix.get() in TIME_LIST_NAME:
            data.append(int(combo_bix.get().split(":")[0]))

        else:
            data.append(int(combo_bix.get()))

    start_date = datetime(year=data[0], month=data[1], day=data[2], hour=data[3])
    end_date = datetime(year=data[4], month=data[5], day=data[6], hour=data[7])

    past_days = data[8]

    netta.netta(start_date, end_date, past_days)


def create_send_button(window, drop_down_list):
    send_button = tk.Button(window, text="GO!", width=8,
                            command=lambda: unpack_and_send_data(drop_down_list), bg='purple', fg='white', font=('Arial', 12))

    send_button.grid(column=3, row=3, padx=10, pady=10)


def run():
    window = tk.Tk()

    create_window(window=window)

    crate_labels(window=window)

    drop_down_list = []
    drop_down_list += create_drop_down_list_for_date(window=window, row="from")
    drop_down_list += create_drop_down_list_for_date(window=window, row="to")
    drop_down_list += create_drop_down_list(window=window)

    create_send_button(window=window, drop_down_list=drop_down_list)

    window.mainloop()

run()
