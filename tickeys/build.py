import shutil
import os
from cx_Freeze import setup, Executable
from __init__ import __version__

buildOptions = dict(
    compressed=True,
    include_files=['kivy', 'tickeys', 'Resources'],)

setup(
    name="tickeys",
    version=__version__,
    description="tickeys alpha version",
    options=dict(build_exe=buildOptions),
    executables=[Executable("run.py")])

# print "Move resources file..."
# shutil.copytree("../Resources", os.getcwd() + "/build/Resources")

print "Add readme file..."
shutil.copyfile("readme.txt", os.getcwd() + "/build/readme.txt")
