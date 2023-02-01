import cx_Freeze

executables = [cx_Freeze.Executable("./Netta - Auto Shifts Generator.py")]

cx_Freeze.setup(
    name="Netta - Auto Shifts Generator",
    executables=executables
    )
