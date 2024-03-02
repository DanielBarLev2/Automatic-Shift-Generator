from src.screen.massage_box import send_file_not_found_error
from src.constants.columns import Columns
from src.algorithms.netta import netta
import win32com.client as win32
from datetime import datetime
import subprocess
import pathlib
import os


def pack_and_send_data(drop_down_list):
    month_list_name = ('January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December')

    time_list_name = ("00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00",
                      "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                      "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00")

    data = []

    for combo_bix in drop_down_list:
        # convert month names into strings
        if combo_bix.get() in month_list_name:
            data.append(month_list_name.index(combo_bix.get()) + 1)

        elif combo_bix.get() in time_list_name:
            data.append(int(combo_bix.get().split(":")[0]))

        else:
            data.append(int(combo_bix.get()))

    start_date = datetime(year=data[0], month=data[1], day=data[2], hour=data[3])
    end_date = datetime(year=data[4], month=data[5], day=data[6], hour=data[7])

    past_days = data[8]

    netta(start_date=start_date, end_date=end_date, past_days=past_days)



def open_workbook():
    workbook_path = Columns.FILE_NAME.value
    try:
        subprocess.call(['start', 'excel.exe', workbook_path], shell=True)
    except FileNotFoundError:
        send_file_not_found_error(Columns.FILE_NAME.value)


def close_workbook():

    # Path of the Excel workbook to open
    workbook_path = Columns.FILE_NAME.value

    # Get the Excel application object
    excel = win32.Dispatch('Excel.Application')

    # Check if the workbook is open
    for wb in excel.Workbooks:
        if wb.FullName == workbook_path:
            wb.Close()

    excel.Quit()


def open_setting():
    path = str(pathlib.Path.cwd().joinpath('src/config/config.ini'))
    path = path.replace(str("\\"), str("/"))

    os.startfile(path)

