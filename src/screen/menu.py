from src.screen.button_functions import *
from src.classes.MyThread import MyThread
from datetime import timedelta
from tkinter import ttk
import tkinter as tk
import calendar


def create_window(window):
    window.geometry("480x350")
    window.title("Netta")
    window.iconbitmap("media/Netta_Art.ico")


def crate_labels(window):
    title_label = tk.Label(window, text="הפקשטומטי של יעלי", font="Times  16")
    title_label.grid(column=1, row=0, columnspan=4, pady=20, padx=40)

    from_label = tk.Label(window, text="From:")
    from_label.grid(column=0, row=1, pady=10, padx=10)

    to_label = tk.Label(window, text="To:")
    to_label.grid(column=0, row=2, pady=10, padx=10)

    to_label = tk.Label(window, text="Take")
    to_label.grid(column=0, row=3, pady=10, padx=10)

    to_label = tk.Label(window, text="days into account")
    to_label.grid(column=2, row=3, pady=10, padx=10)


def create_drop_down_list(window):
    account_drop_down = ttk.Combobox(window, values=tuple(range(0, 8)), width=8, justify="center")
    account_drop_down.grid(column=1, row=3, padx=10, pady=10)
    account_drop_down.current(2)

    return [account_drop_down]


def create_drop_down_list_for_date(window, row: str):
    month_list_name = ('January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December')

    time_list_name = ("00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00",
                      "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                      "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00")

    # create drop down
    year_drop_down = ttk.Combobox(window, values=tuple(range(2020, 2030)), width=8, justify="center")
    month_drop_down = ttk.Combobox(window, values=month_list_name, width=8, justify="center")
    day_drop_down = ttk.Combobox(window, values=tuple(range(1, 32)), width=8, justify="center")
    time_drop_down = ttk.Combobox(window, values=time_list_name, width=8, justify="center")

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

    day_name = calendar.day_name[date.weekday()]

    week_dict = {
        'Saturday': 5,
        'Sunday': 4,
        'Monday': 3,
        'Tuesday': 2,
        'Wednesday': 1,
        'Thursday': 3,
        'Friday': 2
    }

    # adapt the default time delta between 'from date' and 'to date'
    date += timedelta(days=week_dict[day_name])

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


def create_send_button(window, drop_down_list, thread_open_workbook):
    send_button = tk.Button(window, text="Generate", width=8,
                            command=lambda: pack_and_send_data(drop_down_list, thread_open_workbook),
                            bg='purple', fg='white', font=('Arial', 10))

    send_button.grid(column=1, row=4, padx=10, pady=10)


def create_open_workbook_button(window):
    open_button = tk.Button(window, text="Open Excel", width=8,
                            command=lambda: open_workbook(),
                            bg='green', fg='white', font=('Arial', 10))

    open_button.grid(column=2, row=4, padx=10, pady=10)


def create_close_workbook_button(window):
    open_button = tk.Button(window, text="Close Excel", width=8,
                            command=lambda: close_workbook(),
                            bg='red', fg='white', font=('Arial', 10))

    open_button.grid(column=3, row=4, padx=10, pady=10)


def create_open_settings_button(window):
    open_button = tk.Button(window, text="Settings", width=8,
                            command=lambda: open_setting(),
                            bg='blue', fg='white', font=('Arial', 10))

    open_button.grid(column=4, row=4, padx=10, pady=10)


def run():
    window = tk.Tk()

    # starts opening workbook to save time
    thread_open_workbook = MyThread()
    thread_open_workbook.start()

    create_window(window=window)

    crate_labels(window=window)

    drop_down_list = []
    drop_down_list += create_drop_down_list_for_date(window=window, row="from")
    drop_down_list += create_drop_down_list_for_date(window=window, row="to")
    drop_down_list += create_drop_down_list(window=window)

    create_send_button(window=window, drop_down_list=drop_down_list, thread_open_workbook=thread_open_workbook)
    create_open_workbook_button(window=window)
    create_close_workbook_button(window=window)
    create_open_settings_button(window=window)

    window.mainloop()
