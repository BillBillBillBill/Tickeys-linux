import sys
from cx_Freeze import setup, Executable

buildOptions = dict(
        compressed = True,
        includes = ["pygame", "os", "kivy", "sys"],
        include_files = ['kivy'])

setup(
name = "tickeys",
version = "0.1",
description = "tickeys alpha version",
options=dict(build_exe=buildOptions),
executables = [Executable("run.py")])