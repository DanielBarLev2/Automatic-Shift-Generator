from src.algorithms.netta import load_and_divide_workbook
from threading import Thread


class OpenWorkbookThread(Thread):
    """
    This thread class is a custom single purpose class.
    It altered the thread class to obtain a value,
    from a load_and_divide_workbook function.
    """
    # constructor
    def __init__(self):
        """
        Execute the base constructor.
        Add a return value: excel workbook and sheets
        Add a boolean for an up-to-date workbook
        """

        Thread.__init__(self)
        self.value = None

    def run(self):
        """
        open excel workbook in a different thread
        """
        self.value = load_and_divide_workbook()
