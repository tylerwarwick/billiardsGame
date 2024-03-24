import time
import Physics as p
import server as s
import math as m


db = p.Database()


def addStillBall(table, num, x, y):
    ball = p.StillBall(num, p.Coordinate(x, y))
    table += ball

# Helper function to make new table
def newTable():
    # Get blank table obj 
    table = p.Table()

    # Declare reference point
    ref = p.TABLE_WIDTH/2

    # Add cue ball
    addStillBall(table, 0, ref, p.TABLE_LENGTH - ref)
    
    # Add balls 1-15
    # First row
    addStillBall(table, 1, ref, ref)
    # Second row
    addStillBall(table, 2, ref - (p.BALL_DIAMETER+4.0)/2.0, ref-m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))
    addStillBall(table, 3, ref + (p.BALL_DIAMETER+4.0)/2.0, ref-m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))
    # Third row
    addStillBall(table, 4, ref - (p.BALL_DIAMETER+4.0)/2.0 * 2, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*2)
    addStillBall(table, 5, ref, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*2)
    addStillBall(table, 6, ref + (p.BALL_DIAMETER+4.0)/2.0 * 2, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*2)
    # Fourth row
    addStillBall(table, 7, ref - (p.BALL_DIAMETER+4.0)/2.0 * 3, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*3)
    addStillBall(table, 8, ref - (p.BALL_DIAMETER+4.0)/2.0, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*3)
    addStillBall(table, 9, ref + (p.BALL_DIAMETER+4.0)/2.0, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*3)    
    addStillBall(table, 10, ref + (p.BALL_DIAMETER+4.0)/2.0 * 3, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*3)   
    # Final row
    addStillBall(table, 11, ref - (p.BALL_DIAMETER+4.0)/2.0 * 4, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*4)
    addStillBall(table, 12, ref - (p.BALL_DIAMETER+4.0)/2.0 * 2, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*4)
    addStillBall(table, 13, ref, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*4)    
    addStillBall(table, 14, ref + (p.BALL_DIAMETER+4.0)/2.0 * 2, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*4)  
    addStillBall(table, 15, ref + (p.BALL_DIAMETER+4.0)/2.0 * 4, ref - (m.sqrt(3.0) / 2.0 * (p.BALL_DIAMETER+4.0))*4)    
    
    return table

table = newTable()
db = p.Database(True)

game = p.Game(None, "Game", "Tyler", "Erin")

# one writetbale at a time attempt
#db.writeTable(table)
#db.writeTable(table)

# batch write table
#db.batchWriteTable([table, table], 1)

startTime = time.time()
# Old shoot
#svg, shotId = game.shoot("who cares", "Erin", table, 0, -500)
#print(svg)
#print(shotId)

# New shoot
svg, shotId = game.newShoot("who cares", "Erin", table, 0, -500)
#print(svg)
#print(shotId)


print("Time it took: ", time.time() - startTime)

"""
game.shoot("Game", "Erin", table, 0, 0)
game.updateLowBallPlayer(1)
gameId = game.gameID
print("I just made the game and this is player 1: ", game.player1Name, "\n player 2: ", game.player2Name, "\n")
print("Player ", game.lowBallPlayer, " has lowballs\n")
reconstructedTable, playerWhoWentLast = db.latestGameState(1)

game2 = p.Game(gameId)
print("I just fetched this game and this is player 1: ", game2.player1Name, "\n player 2: ", game2.player2Name, "\n")
print("Player ", game2.lowBallPlayer, " has lowballs\n")
"""
