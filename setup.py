import cx_Freeze
import sys
import matplotlib

base = None

# if sys.platform == "win32":
#     base = "Win32GUI"

executables  = [cx_Freeze.Executable("CapoUI.py", base=base, icon="HR_ICON.png")]
include_files = ["aggregation.py", "analyser.py", "HR_ICON.png", "modelpredictor.py", "modeltrainer.py",
                 "preprocessing.py", "scoring.py", "TextBox.py", "utility.py", "Solver/Solver.xlsx"]
cx_Freeze.setup(
    name="Capo - Assistsant",
    options={"build_exe":{"packages":["tkinter", "encodings", "matplotlib", "seaborn", "pandas", "numpy"],
                            "include_files":include_files}},
    version=0.01,
    description="Alpha Testing",
    executables =executables
)