def write_shift_list(ws, shift_list: list, start_row: int, end_row: int, person_col: int):
    """
    Write and place personnel by order from shift list into excel workbook
    :param ws: excel worksheet
    :param shift_list: shift list to place in one column
    :param start_row: points on the first shift in the ws
    :param end_row: points on the last shift in the ws
    :param person_col: the column for placements
    :return:
    """

    for start_row in range(start_row, end_row + 1):
        # places only if the cell is the first in a merged group
        if ws.cell(column=person_col - 1, row=start_row).value is not None:
            # places only if the cell is empty
            if ws.cell(column=person_col, row=start_row).value != " ":
                # is not empty
                if shift_list:
                    ws.cell(column=person_col, row=start_row).value = shift_list.pop(0).person
                else:
                    break

        # continue
        start_row += 1
