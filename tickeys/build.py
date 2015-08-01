import shutil
import os
from cx_Freeze import setup, Executable
from __init__ import __version__

executable_filename = "tickeys"

if __name__ == '__main__':

    buildOptions = dict(
        compressed=True,
        include_files=['kivy', 'tickeys', 'Resources'],)

    setup(
        name=executable_filename,
        version=__version__,
        description='Instant audio feedback when typing. For Linux.',
        options=dict(build_exe=buildOptions),
        executables=[Executable("run.py")])

    # print "Move resources file..."
    # shutil.copytree("../Resources", os.getcwd() + "/build/Resources")

    print "Add readme file..."
    shutil.copyfile("../README.md", os.getcwd() + "/build/README.md")

    print "Add some docs..."
    shutil.copyfile("../AUTHOURS", os.getcwd() + "/build/AUTHOURS")
    shutil.copyfile("../Changelog", os.getcwd() + "/build/Changelog")
    shutil.copyfile("../LICENSE", os.getcwd() + "/build/LICENSE")