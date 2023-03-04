from tkinter import messagebox
from datetime import datetime
import tkinter as tk


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
