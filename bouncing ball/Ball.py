from Constants import Constants
import random
import math
from Racket import Racket
from tkinter import *


class Ball(object):
    RADIUS = 10

    def __init__(self):
        # initiate the location of the ball in the middle of the window
        self.x = 0.5 * Constants.WIDTH
        self.y = 0.5 * Constants.HEIGHT

        # initiate the speed of the ball with random direction and speed 3
        self.speedX = random.randrange(601) / 100 - 3
        self.speedY = math.sqrt(9.0 - self.speedX ** 2)
        self.appear()

    # functions to get and set the location of the ball
    
    # output: the x coordinate of the ball
    def getX(self):
        return self.x
        
    # output: the y coordinate of the ball
    def getY(self):
        return self.y

    # input: the x coordinate of the ball
    def setX(self, x):
        self.x = x

    # input: the y coordinate of the ball
    def setY(self, y):
        self.y = y

    # functions to get the speed of the ball
    # output: the x coordinate speed of the ball
    def getSpeedX(self):
        return self.speedX

    # output: the y coordinate speed of the ball
    def getSpeedY(self):
        return self.speedY

    # input: the x coordinate speed of the ball
    def setSpeedX(self, speedX):
        self.speedX = speedX

    # input: the y coordinate speed of the ball
    def setSpeedY(self, speedY):
        self.speedY = speedY

    # let the ball appear on the screen
    def appear(self):
        self.ball = Constants.canvas.create_oval(self.x - Ball.RADIUS, self.y - Ball.RADIUS,
                                       self.x + Ball.RADIUS, self.y + Ball.RADIUS,
                                       fill="black")

    # check whether the ball is out of bound
    # return the answer of whether is ball is out of bound
    def outOfBoundary(self):
        if self.x - Ball.RADIUS > Constants.RIGHT_BOUND or self.x + Ball.RADIUS < Constants.LEFT_BOUND or self.y - Ball.RADIUS > Constants.DOWN_BOUND or self.y + Ball.RADIUS < Constants.UP_BOUND:
            return True
        else:
            return False

    # check whether the ball is in the right goal entirely
    def goalRight(self, x, y):
        if 360 * Constants.HEIGHT / 1050 < y < 690 * Constants.HEIGHT / 1050 and x - Ball.RADIUS > Constants.RIGHT_BOUND:
            return True
        else:
            return False

    # check whether the ball is in the left goal entirely
    def goalLeft(self, x, y):
        if 360 * Constants.HEIGHT / 1050 < y < 690 * Constants.HEIGHT / 1050 and x + Ball.RADIUS < Constants.LEFT_BOUND:
            return True
        else:
            return False

#    # find the speed after bouncing
#    def bounce(self, x, y, a, b):
#        if x * a + y * b >= 0:
#            return x, y
#
#        r = math.sqrt(x * x + y * y)
#        angleN = math.atan2(b, a)
#        angleV = math.atan2(y, x)
#        angleDifference = self.adjustAngle(angleV - angleN)
#        newAngle = angleN - angleDifference
#        x = r * math.cos(newAngle)
#        y = r * math.sin(newAngle)
#        return x, y

    # adjust the angle to the range from 0 to pi
    def adjustAngle(self, x):
        while x > 0.5 * math.pi:
            x -= math.pi
        while x < -0.5 * math.pi:
            x += math.pi
        return x

    # find out what happens to the ball after colliding with a racket
    def collision(self, racket):
        # compute the locational angle of the ball and the racket and the positive x direction
        x1 = self.x - racket.getX()
        y1 = self.y - racket.getY()
        angleN = math.atan2(y1, x1)

        # compute the angle of relative speed and the positive x direction
        x2 = self.speedX - racket.getSpeedX()
        y2 = self.speedY - racket.getSpeedY()
        r = math.sqrt(x2 * x2 + y2 * y2)
        angleV = math.atan2(y2, x2)
        angleDifference = self.adjustAngle(angleV - angleN)
        newAngle = angleN - angleDifference
        self.speedX = r * math.cos(newAngle)
        self.speedY = r * math.sin(newAngle)

        # rectify the speed of the ball when they collide with the same speed x or y direction
        if abs(self.speedX) < abs(racket.getSpeedX()) or self.speedX * racket.getSpeedX() < 0:
            self.speedX = math.sqrt(racket.getSpeedX() ** 2 + racket.getSpeedY() ** 2) * math.cos(angleN)
        if abs(self.speedY) < abs(racket.getSpeedY()) or self.speedY * racket.getSpeedY() < 0:
            self.speedY = math.sqrt(racket.getSpeedX() ** 2 + racket.getSpeedY() ** 2) * math.sin(angleN)

    # compute the speed of the ball with friction
    def friction(self):
        r = math.sqrt(self.speedX ** 2 + self.speedY ** 2)
        if r > 0.01:
            multi = (r-0.01) / r
            self.speedX *= multi
            self.speedY *= multi
        else:
            self.speedX = 0
            self.speedY = 0

    # check if the ball will collide with a racket
    def willCollide(self, racket):
        if (self.x + self.speedX + racket.speedX - racket.getX()) ** 2 + (self.y + self.speedY + racket.speedY - racket.getY()) ** 2 <= (Ball.RADIUS + Racket.RADIUS) ** 2:
            return True
        else:
            return False
    # implement the motion of 
    def ballMove(self, racket1, racket2):
        flag = False
        # check the location the ball should change speed direction and define the motion correspond to the location
        if self.willCollide(racket2):
            self.collision(racket2)
        elif self.willCollide(racket1):
            self.collision(racket1)
        else:
            if not 360 * Constants.HEIGHT / 1050 < self.y < 690 * Constants.HEIGHT / 1050:
                if self.x + Ball.RADIUS + self.speedX >= Constants.RIGHT_BOUND:
                    self.speedX = -abs(self.speedX)
                elif self.x - Ball.RADIUS + self.speedX <= Constants.LEFT_BOUND:
                    self.speedX = abs(self.speedX)

            if self.y + Ball.RADIUS + self.speedY >= Constants.DOWN_BOUND:
                self.speedY = -abs(self.speedY)
            elif self.y - Ball.RADIUS + self.speedY <= Constants.UP_BOUND:
                self.speedY = abs(self.speedY)

        # add friction and change location
        self.friction()
        self.x += self.speedX
        self.y += self.speedY
        # if goal, reset the game
        if self.outOfBoundary():
            if self.goalRight(self.x, self.y):
                self.x = 1394 * Constants.WIDTH / 1680
                self.y = 0.5 * Constants.HEIGHT
                self.speedX = 0
                self.speedY = 0
                racket1.setX(100)
                racket1.setY(300)
                racket2.setX(800)
                racket2.setY(300)
                racket1.addScore()
                flag = True

            elif self.goalLeft(self.x, self.y):
                self.x = 287 * Constants.WIDTH / 1680
                self.y = 0.5 * Constants.HEIGHT
                self.speedX = 0
                self.speedY = 0
                racket1.setX(100)
                racket1.setY(300)
                racket2.setX(800)
                racket2.setY(300)
                racket2.addScore()
                flag = True

        # visualize the change of the location of the ball
        Constants.canvas.delete(self.ball)
        self.appear()
        # return goal(1) or not(0)
        return flag
