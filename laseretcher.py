#!/usr/bin/env python3

try:
    # for Python3
    import tkinter as tk   ## notice lowercase 't' in tkinter here
    from tkinter.font import Font
    from tkinter import ttk
except ImportError:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter
from functools import partial

#import RPi.GPIO as GPIO

from stream import GrblControl

design = [
    ('Laser UVU Logo', '/home/pi/laseretcher/gcode/uvulogo.gcode'),
    ('Pig',  '/home/pi/laseretcher/gcode/pig.gcode'),
    ('Circle',  '/home/pi/laseretcher/gcode/circle.gcode'),
    ('Names',  '/home/pi/laseretcher/gcode/names.gcode')
    ]

win = tk.Tk()
myFont = Font(family = 'Helvetica', size = 36, weight = 'bold')

win.title("Laser Etcher")
win.geometry('1020x720')

def exitProgram():
    print("Exit Button pressed")
    win.quit()

def run_speedtest():
    subprocess.call('speedtest')

laseretcher = GrblControl("/dev/ttyUSB0")
def stream(filename):
    laseretcher.start(filename)

print ('Hello, world!')

for text, filename in design:
    runButton = tk.Button(win,
        text = text, font = myFont,
        command = partial(stream, filename), height = 1, width = 15)
    runButton.pack(side = tk.TOP)

w = tk.Spinbox(win, from_ = 0, to = 10)
w.pack()

win.mainloop()

