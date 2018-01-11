import time
import threading
from tkinter import *
import random
from PIL import Image, ImageTk
import math
from Ball import Ball
from Racket import Racket
from Constants import Constants


# when user press the different keys, set speed of the rackets
def keydown(event, racket1, racket2):
    if event.keysym == "a":
        racket1.setSpeedX(-3)
    if event.keysym == "d":
        racket1.setSpeedX(3)
    if event.keysym == "w":
        racket1.setSpeedY(-3)
    if event.keysym == "s":
        racket1.setSpeedY(3)

    if event.keysym == "Left":
        racket2.setSpeedX(-3)
    if event.keysym == "Right":
        racket2.setSpeedX(3)
    if event.keysym == "Up":
        racket2.setSpeedY(-3)
    if event.keysym == "Down":
        racket2.setSpeedY(3)


# when user stop pressing the keys, set speed of this direction 0
def keyup(event, racket1, racket2, psd):
    if event.keysym in ["a", "d"]:
        racket1.setSpeedX(0)
    if event.keysym in ["w", "s"]:
        racket1.setSpeedY(0)
    if event.keysym in ["Left", "Right"]:
        racket2.setSpeedX(0)
    if event.keysym in ["Up", "Down"]:
        racket2.setSpeedY(0)
    if event.keysym is "p":
        psd.switch(psd)

def store(racket1, racket2, ball):
    fileOut = open("record.txt", "w")
    print(racket1.getX(), file=fileOut)
    print(racket1.getY(), file=fileOut)
    print(racket2.getX(), file=fileOut)
    print(racket2.getY(), file=fileOut)
    print(ball.getX(), file=fileOut)
    print(ball.getY(), file=fileOut)
    print(ball.getSpeedX(), file=fileOut)
    print(ball.getSpeedY(), file=fileOut)
    print(racket1.getScore(), file=fileOut)
    print(racket2.getScore(), file=fileOut)
    fileOut.close()


def reload(racket1, racket2, ball):
    fileIn = open("record.txt", "r")
    dataList = []
    for line in fileIn:
        line = line.strip()
        dataList.append(line)
    fileIn.close()
    racket1.setX(int(dataList[0]))
    racket1.setY(int(dataList[1]))
    racket2.setX(int(dataList[2]))
    racket2.setY(int(dataList[3]))
    ball.setX(float(dataList[4]))
    ball.setY(float(dataList[5]))
    ball.setSpeedX(float(dataList[6]))
    ball.setSpeedY(float(dataList[7]))
    racket1.setScore(int(dataList[8]))
    racket2.setScore(int(dataList[9]))

    playGame(racket1, racket2, ball)


def playGame(racket1, racket2, ball):
    MenuItems.destroyAll(MenuItems)

    # insert the soccer field background
    img = Image.open("soccer-field-1.jpg")
    img = img.resize((Constants.WIDTH, Constants.HEIGHT), Image.ANTIALIAS)
    tk_img = ImageTk.PhotoImage(img)
    Constants.canvas.create_image(450, 300, image=tk_img)

    # initiate the scoreboard
    scoreBoard = Constants.canvas.create_text(449, 50, fill="black", font=("PT Sans", 30), text=str(racket1.getScore()) + " : " + str(racket2.getScore()))

    # draw helper text
    Constants.canvas.create_text(Constants.WIDTH * 0.5, Constants.HEIGHT * 0.95, fill="gray",
                font=("PT Sans", 12), text='Press direction keys and WASD to move rackets. Press <P> to pause.')

    # relate the rackets to the keyboard
    Constants.rootWindow.bind("<KeyPress>", lambda event: keydown(event, racket1, racket2))
    Constants.rootWindow.bind("<KeyRelease>", lambda event: keyup(event, racket1, racket2, Paused))

    # an object to manage game pauses and items that show up in pause menu
    class Paused(object):
        paused = False
        psText = None
        psImg = None

        # switch between paused state to game state
        def switch(self):
            self.paused = not self.paused
            if self.paused:
                # draw dark soccer field image
                overlay = ImageTk.PhotoImage(Image.open("soccer-field-dark.jpg"))
                overlay = Image.open("soccer-field-dark.jpg")
                overlay = overlay.resize((Constants.WIDTH, Constants.HEIGHT), Image.ANTIALIAS)
                tk_overlay = ImageTk.PhotoImage(overlay)
                Constants.rootWindow.tk_overlay = tk_overlay
                self.psImg = Constants.canvas.create_image(450, 300, image=tk_overlay)

                # draw paused text
                self.psText = Constants.canvas.create_text(Constants.WIDTH/2, Constants.HEIGHT/2, fill="white",
                               font=("PT Sans", 48), text='Paused')
            else:
                # remove items shown on paused view
                Constants.canvas.delete(self.psImg)
                Constants.canvas.delete(self.psText)

    startTime = time.time()
    while True:

        # draw items when game is not paused
        if Paused.paused is False:
            start = time.time()
            racket1.racketMove()
            racket2.racketMove()
            goal = ball.ballMove(racket1, racket2)
            if goal:
                Constants.canvas.delete(scoreBoard)
                scoreBoard = Constants.canvas.create_text(449, 50, fill="black", font=("PT Sans", 30),
                                                          text=str(racket1.getScore()) + " : " + str(racket2.getScore()))
            Constants.rootWindow.update()
            end = time.time()

            if end - startTime > 1:
                store(racket1, racket2, ball)
                startTime = end

            if end - start < 0.01:
                time.sleep(0.01 + start - end)

        # draw items when game is paused
        else:
            # redraw score board to white color
            pauseScoreBoard = Constants.canvas.create_text(449, 50, fill="white", font=("PT Sans", 30),
                                        text=str(racket1.getScore()) + " : " + str(racket2.getScore()))
            Constants.rootWindow.update()
            startTime = time.time()
            time.sleep(0.1)
            Constants.canvas.delete(pauseScoreBoard)

# a class that wraps up all menu items for convenience
class MenuItems(object):
    # init all items to none
    bg = None
    title = None
    newGameButton = None
    reloadGameButton = None
    newHover = None
    reloadHover = None

    # remove all items shown in menu
    def destroyAll(self):
        Constants.canvas.delete(self.bg)
        Constants.canvas.delete(self.title)
        Constants.canvas.delete(self.newGameButton)
        Constants.canvas.delete(self.reloadGameButton)

# draw items shown on the menu
def drawMenu(racket1, racket2, ball):

    # background of menu page
    menu_bg = Image.open("field-bg.jpg")
    menu_bg = menu_bg.resize((Constants.WIDTH, Constants.HEIGHT), Image.ANTIALIAS)
    tk_menu_bg = ImageTk.PhotoImage(menu_bg)
    Constants.rootWindow.tk_menu_bg = tk_menu_bg
    MenuItems.bg = Constants.canvas.create_image(450, 300, image=tk_menu_bg)

    # "Bouncing Ball" Title
    MenuItems.title = Constants.canvas.create_text(Constants.WIDTH * 0.5, Constants.HEIGHT * 0.35, fill="black",
                                               font=("PT Sans", 48), text='Bouncing Ball')

    # Clickable text New Game and Reload
    MenuItems.newGameButton = Constants.canvas.create_text(Constants.WIDTH * 0.5, Constants.HEIGHT * 0.7, fill="white",
                                        font=("PT Sans", 24), text='New Game', tags="new")
    MenuItems.reloadGameButton = Constants.canvas.create_text(Constants.WIDTH * 0.5, Constants.HEIGHT * 0.8, fill="white",
                                        font=("PT Sans", 24), text='Reload', tags="reload")

    # Bind texts to actions
    Constants.canvas.tag_bind("new", "<Button-1>", lambda foo: playGame(racket1, racket2, ball))
    Constants.canvas.tag_bind("reload", "<Button-1>", lambda foo: reload(racket1, racket2, ball))

def main():
    Constants.rootWindow.title("Bouncing Ball")

    # create the ball and rackets
    ball = Ball()
    racket1 = Racket(100, 300)
    racket2 = Racket(800, 300)

    Constants.rootWindow.geometry(str(Constants.WIDTH)+"x"+str(Constants.HEIGHT))
    Constants.rootWindow.resizable(width=False, height=False)

    Constants.canvas.pack()

    # draw menu
    drawMenu(racket1, racket2, ball)

    Constants.rootWindow.mainloop()

    # playGame(racket1, racket2, ball)



main()
