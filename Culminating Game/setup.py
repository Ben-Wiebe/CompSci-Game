from cx_Freeze import setup, Executable
import os

includes = ["pygame",
            "settings",
            "functions",
            "classes",
            "math",
            "random",
            "Maze",
            "copy",
            "ctypes",
            "caves"]

setup(options = {"build_exe": {"includes": includes} } ,
      name = "The Grand Labyrinth" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("Main.py", base = "Win32GUI")])
