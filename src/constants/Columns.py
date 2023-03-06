from configparser import ConfigParser
from datetime import timedelta
from enum import Enum
import pathlib


def set_path_confiig() -> ConfigParser:
    # get relative path of config.ini file
    path = str(pathlib.Path.cwd().joinpath('src/config/config.ini'))
    path = path.replace(str("\\"), str("/"))

    # set config file as config
    config = ConfigParser()
    config.read(path, encoding="utf8")

    return config


class Columns(Enum):

    config: ConfigParser = set_path_confiig()

    # path for config
    FILE_NAME = config['path']['file_name']

    # shift sheet
    SHIFT_SHEET_NAME = config['shift_sheet']['sheet_name']

    DATE = int(config['shift_sheet']['date_col'])
    CONTROL_TIME = int(config['shift_sheet']['control_time_col'])
    CONTROL_PERSON = int(config['shift_sheet']['control_person_col'])
    GUARD_TIME = int(config['shift_sheet']['guard_time_col'])
    GUARD_PERSON = int(config['shift_sheet']['guard_person_col'])
    ATTENDANCE = int(config['shift_sheet']['attendance_col'])
    DEPARTURE = int(config['shift_sheet']['departure'])
    ARRIVAL = int(config['shift_sheet']['arrival'])

    # personnel sheet
    PERSONNEL_SHEET_NAME = config['personnel_sheet']['sheet_name']

    CONTROL_SUPPORT = int(config['personnel_sheet']['control_support_col'])
    GUARD_SUPPORT = int(config['personnel_sheet']['guard_support_col'])
    FIRST_PERSONNEL_ROW = int(config['personnel_sheet']['first_personnel_row'])

    # config sheet
    START_DATE = str(config['config_sheet']['start_date'])
    END_DATE = str(config['config_sheet']['end_date'])
    START_TIME = str(config['config_sheet']['start_time'])
    END_TIME = str(config['config_sheet']['end_time'])

    # back counting shift list days
    PAST_DAYS = int(config['past']['reference'])

    # config sheet
    CONFIG_SHEET_NAME = config['config_sheet']['sheet_name']

    # set by default to 8 hours
    MAX_GAP = timedelta(0, 0, 0, 0, 0, int(config['gap']['max_gap']), 0)

    # Merge cells number grouped in date column
    DATE_CELL_SIZE = int(config['date_cell']['size'])

    MAX_ROW_LIMIT = 10_000

    DAY_START = 8
    NIGHT_START = 0
    DAY_END = 24
