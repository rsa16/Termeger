import sys
from cx_Freeze import setup, Executable

base = None


setup(
    name="Termeger",
    version = "0.1",
    description="A TUI application for instant messaging (sort of)",
    executables = [Executable("main.py", base=base)]
)
