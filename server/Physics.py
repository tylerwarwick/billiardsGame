import phylib;
import os;
import sqlite3;
import math as m;


################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_INTERVAL = 0.01

# web server SVG constants
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""

FOOTER = """</svg>\n"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, 
                                       None, 
                                       None, 
                                       0.0, 
                                       0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall


    # SVG method
    def svg( self ):
        #Dereference object
        pos = self.obj.still_ball.pos

        # Append id tag if cueball for backend
        if (self.obj.still_ball.number == 0):
            return """ <circle id="cueBall" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (pos.x, pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])


        #Return svg representation
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (pos.x, pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position, 
        velocity and acceleration as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, 
                                       vel, 
                                       acc, 
                                       0.0, 
                                       0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall


    # SVG method
    def svg( self ):
        #Dereference object
        pos = self.obj.rolling_ball.pos

        # Append id tag if cueball for backend
        if (self.obj.rolling_ball.number == 0):
            return """ <circle id="cueBall" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (pos.x, pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        
        #Return svg representation
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (pos.x, pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires position only 
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       None, 
                                       pos, 
                                       None, 
                                       None, 
                                       0.0, 
                                       0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole


    # SVG method
    def svg( self ):
        #Dereference object
        pos = self.obj.hole.pos

        #Return svg representation
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (pos.x, pos.y, HOLE_RADIUS)
        

class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires y position only 
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       None, 
                                       None, 
                                       None, 
                                       None, 
                                       0.0, 
                                       y );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion


    # SVG method
    def svg( self ):
        # Declare y value
        y = self.obj.hcushion.y
        if (y == 0):
            y = -25

        #Return svg representation
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y)

class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires x position only 
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       None, 
                                       None, 
                                       None, 
                                       None, 
                                       x,
                                       0.0 ) 
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion


    # SVG method
    def svg( self ):
        # Declare x value
        x = self.obj.vcushion.x
        if (x == 0):
            x = -25

        #Return svg representation
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # SVG method
    def svg( self ):
        #Return svg representation
        returnString = "";

        #Append header
        returnString += HEADER

        #Append svg for each object
        for object in self:
            if (object is not None):
                returnString += object.svg()

        #Append footer
        returnString += FOOTER

        #Return final SVG string
        return returnString
    
    def roll( self, t ):
        new = Table()

        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) )
            
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t )

                # add ball to table
                new += new_ball
              
        
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y ) )
                # add ball to table
                new += new_ball
        
        # return table
        return new
    
    # Fetch cueBall object
    # Absolutely hate this syntax style but have to be filthy here
    def cueBall(self):
        # Need to do it this way because exiting for loop early breaks
        # the given iter overloaded method provided
        returnVal = None

        for obj in self:
            # Find cue ball and return it
            if (obj.__class__ is StillBall and obj.obj.still_ball.number == 0):
                returnVal = obj, obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y
            
            if (obj.__class__ is RollingBall and obj.obj.rolling_ball.number == 0):
                returnVal = obj, obj.obj.rolling_ball.pos.x, obj.obj.rolling_ball.pos.y
                
        # Return nothing or the cue
        return returnVal
    
class Database:

    # Define constructor 
    def __init__(self, reset=False):
        # If we set reset flag to true delete db 
        if (reset == True and os.path.exists('./phylib.db')):
            os.remove('./phylib.db')

        # Get a connection
        self.conn = sqlite3.connect('./phylib.db')

        # Create db if we don't have one (built in)
        self.createDB()  

    # Create database method 
    def createDB(self):
        # Get db cursor 
        cur = self.conn.cursor()

       # Make ball table
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Ball 
            ( 
                BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                BALLNO  INTEGER NOT NULL,
                XPOS    FLOAT NOT NULL,
                YPOS    FLOAT NOT NULL,
                XVEL    FLOAT,
                YVEL    FLOAT
                );"""
        )

        # Make Table Table (real naming convention here)
        cur.execute( 
            """CREATE TABLE IF NOT EXISTS TTable
            (  
                TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIME FLOAT NOT NULL
            );"""
        ) 

        # Make BallTable table
        cur.execute( 
            """CREATE TABLE IF NOT EXISTS BallTable
            (  
                BALLID INTEGER NOT NULL,
                TABLEID INTEGER NOT NULL,
                FOREIGN KEY(BALLID) REFERENCES Ball
                FOREIGN KEY(TABLEID) REFERENCES TTable
            );"""
        ) 


        # Make shot table
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Shot
            (  
                SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                PLAYERID INTEGER NOT NULL,
                GAMEID INTEGER NOT NULL,
                FOREIGN KEY(PLAYERID) REFERENCES Player
                FOREIGN KEY(GAMEID) REFERENCES Game 
            );"""
        )

        # Create table of table snapshot
        cur.execute(
            """CREATE TABLE IF NOT EXISTS TableShot 
            (
                TABLEID INTEGER NOT NULL,
                SHOTID INTEGER NOT NULL,
                FOREIGN KEY(TABLEID) REFERENCES TTable 
                FOREIGN KEY(SHOTID) REFERENCES Shot 
            );"""
        )

        # Create table of games
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Game 
            (
                GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMENAME VARCHAR(64) NOT NULL
            );"""
        )

        # Create Player table
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Player 
            (
                PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMEID INTEGER NOT NULL,
                PLAYERNAME VARCHAR(64) NOT NULL,
                FOREIGN KEY(GAMEID) REFERENCES Game 
            );"""
        )
        

        # Commit changes
        self.conn.commit()

        # Close off cursor
        cur.close()

    # Get table from db 
    def readTable(self, tableID):
        # Get cursor
        cur = self.conn.cursor()

        # Instantiate table
        table = Table()

        # Now get actual table info
        query = """
                SELECT BallTable.*, BALLNO, XPOS, YPOS, XVEL, YVEL
                FROM BallTable
                INNER JOIN Ball ON BallTable.BALLID = Ball.BALLID
                WHERE TABLEID = ?
                ORDER BY Ball.BALLID
                """

        # Store results to be worked with 
        data = cur.execute(query, (tableID+1,)).fetchall()
    
        # If we get no results, return none
        if (not data):
            return None

        # Query to get table time (only do so after checking this table exists above)
        table.time = cur.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID + 1,)).fetchone()[0]   

        # Now put into actual table to be returned
        for row in data:
            # Is it still or rolling:
            if (row[5] is None):
                # Make still ball and append to table
                sb = StillBall(row[2], Coordinate(row[3], row[4]))
                table += sb

            else:
                # Get vector magnitude for speed
                speed = m.sqrt((row[5] * row[5]) + (row[6] * row[6]))

                # Only set non-zero acceleration if speed > epsilon
                xAcc = ((-row[5] / speed)  * DRAG) if (speed > phylib.PHYLIB_VEL_EPSILON) else 0
                yAcc = ((-row[6] / speed)  * DRAG) if (speed > phylib.PHYLIB_VEL_EPSILON) else 0
                

                rb = RollingBall(row[2], Coordinate(row[3], row[4]), 
                                 Coordinate(row[5], row[6]), 
                                 Coordinate(xAcc, yAcc)
                                 )
                table += rb

        # Commit connection and close cursor
        self.conn.commit()
        cur.close()


        # Return new table
        return table

        


    # Get table from db 
    def writeTable(self, table):
        # Get cursor
        cur = self.conn.cursor()

        # Make new table in TTable
        cur.execute("INSERT INTO TTable (TIME) VALUES (?) RETURNING TABLEID;", (table.time,))

        # Get newly created tableId
        tableId = cur.fetchone()[0]

        # Insert balls
        for item in table:
            # Only do something if it's ball
            if (isinstance(item, (StillBall, RollingBall))): 
                # Get object for easy to access to props
                # Declare here and set based on still or rolling
                ball = None 
                velX = None
                velY = None

                # None val is not maintained when casted to 
                if (isinstance(item, StillBall)):
                    # Assign still ball to object
                    ball = item.obj.still_ball

                    # Give no velocities
                    velX = None
                    velY = None 
                
                # Otherwise we have rolling ball
                else:
                    # Assign as rolling ball
                    ball = item.obj.rolling_ball
                    velX = ball.vel.x
                    velY = ball.vel.y

                # Put ball info into ball table
                cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?) RETURNING BALLID;", (ball.number,
                                                                                                                           ball.pos.x,
                                                                                                                           ball.pos.y,
                                                                                                                           velX,
                                                                                                                           velY))

                # Get primary ID of new ball
                ballId = cur.fetchone()[0]

                # Put ball into BallTable
                cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ballId, tableId)) 


        # Commit connection and close cursor
        self.conn.commit()
        cur.close()

        # Return tableId (in 0 index context)
        return tableId - 1

    # Get game method for game class
    def getGame(self, gameID):
        # Need cursor
        cur = self.conn.cursor()

        # Fetch game info from db
        query = """
                SELECT Game.*, PLAYERID, PLAYERNAME
                FROM Game
                JOIN Player ON Game.GAMEID = Player.GAMEID
                WHERE Game.GAMEID = ?
                ORDER BY Player.PLAYERID
                """
        
        # Call query
        data = cur.execute(query, (gameID,)).fetchall()

        # Commit and close
        self.conn.commit()
        cur.close()

        # Return game name, and both players name
        return data[0][1], data[0][3], data[1][3]

    # Set game method to create new game
    def setGame(self, gameName, player1Name, player2Name):
        # Need cursor
        cur = self.conn.cursor()

        # Create game new game instance
        cur.execute("INSERT INTO Game (GAMENAME) VALUES (?) RETURNING GAMEID;", (gameName,))

        # Retrieve gameID for use with player creation
        gameID = cur.fetchone()[0]

        # Add player 1 to players table
        cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name)) 

        # Add player 2 to players table
        cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name)) 

        # Commit and close
        self.conn.commit()
        cur.close()

        # Pass gameID back to game instance caller (Decrement for 0 indexing?)
        return gameID

    # New shot for shoot class
    def newShot(self, gameId, playerName):
        # Get cursor
        cur = self.conn.cursor()

        # Get player id
        query = """
                SELECT PLAYERID
                FROM Player
                WHERE GAMEID = ? AND PLAYERNAME = ?
                """
        
        # Get game and player ids for new shot
        playerId = cur.execute(query, (gameId, playerName,)).fetchone()[0]

        # Make new shot in shot table
        cur.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?) RETURNING SHOTID", (playerId, gameId)) 

        # Get shotid from response
        shotId = cur.fetchone()[0]

        # Close and commit 
        self.conn.commit()
        cur.close()

        # Return shotId
        return shotId      

    # Method for inserting into TableShot
    def tableShot(self, tableId, shotId):
        # Get cursor
        cur = self.conn.cursor()

        # Insert into db (increment tableId)
        cur.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (tableId + 1, shotId)) 

        # Close and commit
        self.conn.commit()
        cur.close()

    # Method for finding latest table given a gameId
    def latestGameState(self, gameId):
        # Get cursor
        cur = self.conn.cursor()
        
        # Query for most recent state of table
        query = """
                SELECT TABLEID, PLAYERID
                FROM Shot
                LEFT JOIN TableShot on Shot.SHOTID = TableShot.SHOTID
                WHERE GAMEID = ? 
                ORDER BY shot.SHOTID DESC, TABLEID DESC
                LIMIT 1 
                """

        data = cur.execute(query, (gameId,)).fetchone()
        
        # Get latest table
        latestTable = self.readTable(data[0])

        # Need to find most recent player to shoot
        mostRecentPlayerId = data[1]

        # Want to find who's turn it is
        thisPlayersTurn = cur.execute("""SELECT PLAYERNAME 
                                         FROM Player 
                                         WHERE GAMEID = ? AND PLAYERID != ?
                                      """, (gameId, mostRecentPlayerId))
        
        # Return most recent table and who's turn it is
        return latestTable, thisPlayersTurn


    # Close method
    def close(self):
        self.conn.commit()
        self.conn.close()




class Game:
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        # Need a db instance to work with
        db = Database()

        # First constructor format
        if (gameID is not None and gameName is None and player1Name is None and player2Name is None):
            # For this constructor we know the gameID
            self.gameID = gameID + 1

            # Get game data from db
            [gName, p1, p2] = db.getGame(gameID+1)

            # Populate attributes
            self.gameName = gName
            self.player1Name = p1
            self.player2Name = p2

            # Commit and close
            db.close()

        # Second constructor format
        elif (gameID is None and gameName is not None and player1Name is not None and player2Name is not None):
            # Set attributes 
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

            # Put in db
            # Set unique game id attribute after creating it
            self.gameID = db.setGame(gameName, player1Name, player2Name)

            # Commit and close
            db.close()

        # If neither are met, raise a type error
        else:
            # Commit and close
            db.close()
            
            raise TypeError

    def shoot(self, gameName, playerName, table, xvel, yvel):
        # If table is None, we can't do anything
        if (table is None):
            return None

        # Get db instance
        db = Database()

        # Add entry to shot table in db and get shotId
        shotId = db.newShot(self.gameID, playerName)

        # Get cue ball
        [cueBall, xPos, yPos] = table.cueBall()

        # Store parameters across type conversion
        cueBall.type = phylib.PHYLIB_ROLLING_BALL

        # Refresh values of newly typecast cue ball
        cueBall.obj.rolling_ball.number = 0 
        cueBall.obj.rolling_ball.pos.x = xPos
        cueBall.obj.rolling_ball.pos.y = yPos
        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel

        # Get vector magnitude for speed
        speed = m.sqrt((xvel * xvel) + (yvel * yvel))

        # Only set non-zero acceleration if speed > epsilon
        xAcc = ((-xvel / speed)  * DRAG) if (speed > phylib.PHYLIB_VEL_EPSILON) else 0
        yAcc = ((-yvel / speed)  * DRAG) if (speed > phylib.PHYLIB_VEL_EPSILON) else 0
  
        cueBall.obj.rolling_ball.acc.x = xAcc 
        cueBall.obj.rolling_ball.acc.y = yAcc
                 
        # Fill in segment gaps
        while (table):
            # Save original time
            startTime = table.time

            # Save old table to simulate from as well
            startTable = table

            # Run segment and get updated table
            table = table.segment()

            # Check if we are done iterating
            if (table is None):
                break 

            # Get time elapsed and number of frames
            frames = m.floor((table.time - startTime) / FRAME_INTERVAL)

            # Make a table for each frame in this segment of time
            for i in range(0, frames+1):
                # Get new table with roll applied
                newTable = startTable.roll(i * FRAME_INTERVAL)
              
                # Set its time correctly
                newTable.time = startTime + (i * FRAME_INTERVAL)

                # Write this table to db
                newTableId = db.writeTable(newTable)

                # Also record it in tableshot table
                db.tableShot(newTableId, shotId)

        # Commit and close
        db.close()







