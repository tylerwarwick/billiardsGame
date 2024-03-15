import Physics as p
import math as m
import os


def addStillBall(table, num, x, y):
    ball = p.StillBall(num, p.Coordinate(x, y))
    table += ball

# Get blank table obj 
table = p.Table()

# Declare reference point
ref = p.TABLE_WIDTH/2

# Add cue ball
addStillBall(table, 0, ref, p.TABLE_LENGTH - ref)
    
# Add balls 1-15
addStillBall(table, 1, ref, ref)
addStillBall(table, 2, ref - (p.BALL_DIAMETER+4.0)/2.0, ref-m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))
addStillBall(table, 3, ref + (p.BALL_DIAMETER+4.0)/2.0, ref-m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))
addStillBall(table, 4, ref - (p.BALL_DIAMETER+12.0)/2.0 * 1.5, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*2)
addStillBall(table, 5, ref, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*2)
addStillBall(table, 6, ref + (p.BALL_DIAMETER+4.0)/2.0 * 1.5, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*2)
    

    
if (os.path.exists("./test.svg")):
    os.remove('./test.svg')

with open('test.svg', 'w') as file:
    # Create file
    file.write(table.svg())