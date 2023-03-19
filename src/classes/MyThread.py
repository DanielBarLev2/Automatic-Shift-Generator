from src.algorithms.netta import load_and_divide_workbook
from threading import Thread


class MyThread(Thread):
    """
    This thread class is a custom single purpose class.
    It altered the thread class to obtain a value from a specific function.
    """
    # constructor
    def __init__(self):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.value = None

    # function executed in a new thread
    def run(self):
        self.value = load_and_divide_workbook()
