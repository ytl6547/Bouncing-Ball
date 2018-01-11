from tkinter import *
class Constants(object):
    # width and height of the window
    WIDTH = 900
    HEIGHT = 600

    # soccer field bounds
    RIGHT_BOUND = 852
    LEFT_BOUND = 48
    UP_BOUND = 13
    DOWN_BOUND = 586

    # window and canvas
    rootWindow = Tk()
    canvas = Canvas(rootWindow, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0, relief='ridge')
