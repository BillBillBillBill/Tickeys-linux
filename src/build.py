import sys
import shutil
import os
from cx_Freeze import setup, Executable

buildOptions = dict(
    compressed=True,
    includes=["pygame", "os", "sys"],
    include_files=['kivy', 'run.sh'])

setup(
    name="tickeys",
    version="0.0.1",
    description="tickeys alpha version",
    options=dict(build_exe=buildOptions),
    executables=[Executable("run.py")])

print "Move resources file..."
shutil.copytree("../Resources", os.getcwd() + "/build/Resources")
