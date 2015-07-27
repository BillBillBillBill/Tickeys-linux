import shutil
import os
from cx_Freeze import setup, Executable

buildOptions = dict(
    compressed=True,
    include_files=['kivy', 'tickeys'],)

setup(
    name="tickeys",
    version="0.0.1",
    description="tickeys alpha version",
    options=dict(build_exe=buildOptions),
    executables=[Executable("run.py")])

print "Move resources file..."
shutil.copytree("../Resources", os.getcwd() + "/build/Resources")

print "Add readme file..."
shutil.copyfile("readme.txt", os.getcwd() + "/build/readme.txt")
