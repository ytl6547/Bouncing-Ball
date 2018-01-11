from Constants import Constants
class Racket(object):
    RADIUS = 30

    def __init__(self, x, y):
        self.score = 0
        self.speedX = 0
        self.speedY = 0
        self.x = x
        self.y = y
        self.appear()

    # functions to get and set the location of the racket
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    # functions to get and set the speed of the rackets
    def getSpeedX(self):
        return self.speedX

    def getSpeedY(self):
        return self.speedY

    def setSpeedX(self, speedX):
        self.speedX = speedX

    def setSpeedY(self, speedY):
        self.speedY = speedY

    # functions to add and get score of a player
    def addScore(self):
        self.score += 1

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    # let the racket appear on the screen
    def appear(self):
        self.racket = Constants.canvas.create_oval(self.x - Racket.RADIUS, self.y - Racket.RADIUS,
                                         self.x + Racket.RADIUS, self.y + Racket.RADIUS,
                                         width=5)

    def racketMove(self):
        # control the racket move by delete the racket from the canvas first and draw it again.
        Constants.canvas.delete(self.racket)

        # constrain racket moving range inside the window
        if self.x + Racket.RADIUS + self.speedX >= Constants.WIDTH \
                or self.x - Racket.RADIUS + self.speedX <= 0:
            self.speedX = 0
        if self.y + Racket.RADIUS + self.speedY >= Constants.HEIGHT \
                or self.y - Racket.RADIUS + self.speedY <= 0:
            self.speedY = 0

        self.x += self.speedX
        self.y += self.speedY
        self.appear()
