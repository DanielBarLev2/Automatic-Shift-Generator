from tkinter import messagebox
import tkinter as tk

from src.list_aid.complete import is_complete


def send_end_massage():
    """
    send an end message
    """
    massage = "Done"
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Success", massage)


def send_failed_massage(shift_list: list):
    """
    send a failed message
    """
    if not is_complete(shift_list):

        massage = "Something went wrong. \nCheck your inputs again. \n"
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Failed", massage)

        return False
    else:
        return True


def send_invalid_person_name_error(invalid_shift_list: list) -> bool:
    """
    send an invalid person name message
    :param invalid_shift_list: list of incorrect shift's name
    """
    massage = ""

    if invalid_shift_list:
        for shift in invalid_shift_list:
            massage += f'*{shift.person}* is not exists in personnel sheet or was spelled incorrectly ' \
                       f'at {shift.time_range} \n'

        massage += '\n Do you wish to continue anyway?'

        root = tk.Tk()
        root.withdraw()
        return messagebox.askokcancel("person name error", massage)
    else:
        return True


def send_invalid_availability_name_error(invalid_person_list: list):
    """
    send an invalid availability person name message
    :param invalid_person_list: list of incorrect person's name
    """
    massage = ""

    if invalid_person_list:
        for person in invalid_person_list:
            massage += f'*{person}* is not exists in personnel sheet or was spelled incorrectly at availability ' \
                       f'column. \n '

        massage += '\n Do you wish to continue anyway?'

        root = tk.Tk()
        root.withdraw()
        return messagebox.askokcancel('Availability name error', massage)
    else:
        return True


def send_time_set_error(error: str):
    """
    send a time setting message
    :param error: error type
    """
    if error != 'No errors':
        massage = error
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Setup error", massage)
        return False
    else:
        return True


def send_open_file_error():
    """
    send an open file error
    """
    massage = "The Workbook is currently open. \nClose it to continue."
    root = tk.Tk()
    root.withdraw()

    return messagebox.showinfo("opened file error", massage, icon=messagebox.WARNING, type=messagebox.OKCANCEL)


def send_file_not_found_error(path):
    """
    send a file not found error
    """
    massage = f'The Worksheet cannot be found at {path}. \nrelocate Worksheet path or update it.'
    root = tk.Tk()
    root.withdraw()

    return messagebox.showinfo("file not found", massage, icon=messagebox.WARNING, type=messagebox.OKCANCEL)


def send_not_enough_personnel_warning(personnel_list: list):
    """
    send a not enough personnel warning
    """

    count_available = 0

    for person in personnel_list:
        if person.control_support:
            count_available += 1

    if count_available < 3:
        massage = f'warning! there might Not be enough personnel to preform. \nCurrently only {count_available} are ' \
                  f'(is) supporting Control Shifts'

        root = tk.Tk()
        root.withdraw()

        return messagebox.askokcancel("Personnel warning", massage, icon=messagebox.WARNING, type=messagebox.OKCANCEL)
    else:
        return True


def send_not_complete_past_error(shift_list, start_shift):
    if not is_complete(shift_list[0:start_shift]):
        massage = "You selected a time period too far away. \nNot all past shift are filled."
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Failed", massage)

        return False
    else:
        return True
