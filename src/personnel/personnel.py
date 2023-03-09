from src.classes.Person import Person
from src.constants.columns import Columns


def create_personnel_list(ws) -> list:
    """
    Creates a list with Person class object.
    :param ws: excel personnel worksheet
    :return: list of personnel
    """

    personnel_list = []

    # this column contains values about whether the person is included in the personnel or not
    control_support_col = Columns.CONTROL_SUPPORT.value
    guard_support_col = Columns.GUARD_SUPPORT.value

    row = Columns.FIRST_PERSONNEL_ROW.value

    while ws.cell(column=control_support_col, row=row).value is not None and\
            ws.cell(column=guard_support_col, row=row).value is not None:

        # alter the support attribute accordingly
        if ws.cell(column=control_support_col, row=row).value == "כן":
            control_support = True
        else:
            control_support = False
            
        if ws.cell(column=guard_support_col, row=row).value == "כן":
            guard_support = True
        else:
            guard_support = False

        personnel_list.append(Person(name=ws.cell(column=(control_support_col + 1), row=row).value,
                                     control_support=control_support, guard_support=guard_support))
        row += 1

    return personnel_list
