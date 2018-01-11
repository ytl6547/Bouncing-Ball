Run "bouncing ball.py"

Required libraries:
Tkinter
Pillow: download directly via Preferences -> Project -> Project Interpreter in PyCharm
 
There are 3 classes in my program:
Ball
Racket
Constant
 
The bouncing ball.py, including the main function, is to operate the whole program. In the main function, I create the ball, racket1, and racket2 and drew the menu which asks the use to choose from starting new game or reload the last game. After choosing, the keyboard is related to the rackets. Then the Move functions of the rackets and the ball are initiated. If the ball collides with a racket, the get functions of the Racket will be used to obtain the data of the racket, such as the location and the speed. The constants in the Constants is used by all the other classes if needed.
 
I used tkinter to implement the user interface and the objects on it, the PIL to insert the image to my window. All the other works including the physical engines are the work of myself.