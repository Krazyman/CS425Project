from cx_Freeze import setup, Executable
import os.path
import sys

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None    

executables = [Executable("scheduling.py", base=base)]

packages = ["idna", "operator", "tkinter", "funcs", "os", "PIL"]
options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
         ],
    },
}

setup(
    name = "Scheduling Program",
    options = options,
    author = "Manwai Nguyen",
    author_email = "omitted",
    version = "1.0",
    description = 'Micronesian Brokers Inc. scheduling program',
    executables = executables
)