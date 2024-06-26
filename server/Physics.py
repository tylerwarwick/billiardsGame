import random
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
<svg height="70vh" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">"""

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
 
    def __eq__(self, otherBall) -> bool:
        # If classes or number don't match, they are not equal
        # If number doesn't match, they are not equal
        if (isinstance(otherBall, StillBall)):
            return self.obj.still_ball.number == otherBall.obj.still_ball.number

        return self.obj.still_ball.number == otherBall.obj.rolling_ball.number

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

    # Need number only comparison
    def __eq__(self, otherBall) -> bool:
        # If number doesn't match, they are not equal
        if (isinstance(otherBall, StillBall)):
            return self.obj.rolling_ball.number == otherBall.obj.still_ball.number

        return self.obj.rolling_ball.number == otherBall.obj.rolling_ball.number



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
        # Need to make num 0 instead of None
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
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
        # Need to make num 0 instead of None
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
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
        # Need to make num 0 instead of None
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
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
    def svg(self, header=True):

        returnString = ""

         #Append header
        if header:
            returnString += HEADER

        #Return svg representation
        returnString = returnString + """<rect width="1365" height="2715" x="-10" y="-10" fill="#064e3b" />""";

       

        #Append svg for each object
        for object in self:
            if (object is not None):
                returnString += object.svg()

        #Append footer
        if header:
            returnString += FOOTER

        #Return final SVG string
        return returnString
    
    def roll( self, t ):
        new = Table()

        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                ballObj = ball.obj.rolling_ball                

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
    
    # We'll fetch both the cue ball and 8 ball to save an iteration
    def fetchImportantBallStatuses(self):
        cueBall, eightBall = False

        for obj in self:
            # Find cue ball and return it
            if (obj.__class__ is StillBall and obj.obj.still_ball.number == 0):
                cueBall = True
                
            if (obj.__class__ is StillBall and obj.obj.rolling_ball.number == 8):
                eightBall = True

        return cueBall, eightBall

    # How many balls we have for shoot method    
    def ballCount(self):
        count = 0
        
        for obj in self:
           if (obj.__class__ is StillBall or obj.__class__ is RollingBall):
                count = count + 1

        return count 

    def lowAndHighBalls(self):
        lowBalls = []
        highBalls = []

        for obj in self:
            if (not (isinstance(obj, StillBall) or isinstance(obj, RollingBall))):
                continue
            
            # If it's ball add to appropriate list
            num = getBallNumber(obj)
            if (num < 8 and num != 0):
                lowBalls.append(num)
            if (num >= 9):
                highBalls.append(num)

        return lowBalls, highBalls

    
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
                GAMENAME VARCHAR(64) NOT NULL,
                LOWBALLPLAYER INTEGER,
                WINNER INTEGER,
                WHOSTURNITIS INTEGER NOT NULL
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
        # ** TRY TO GET RID OF ARBITRARY ID OFFSETS
        data = cur.execute(query, (tableID,)).fetchall()
    
        # If we get no results, return none
        if (not data):
            print("Unsuccesful read is returning none")
            return None

        # Query to get table time (only do so after checking this table exists above)
        # ** TRY TO GET RID OF ARBITRARY ID OFFSETS
        table.time = cur.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID,)).fetchone()[0]   

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

        # We will optimize by maintaining a list of queries and doing excecute many
        queriesVals = []

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
                queriesVals.append((ball.number, ball.pos.x, ball.pos.y, velX, velY))
             

        # Excecute all these queries at once
        startingBallId = cur.execute("SELECT BALLID FROM Ball ORDER BY BALLID DESC LIMIT 1").fetchone()
        # If db is brand new we need to None check startingId
        if (startingBallId is None):
            startingBallId = 1
        else:
            startingBallId = startingBallId[0] + 1

        
        cur.executemany("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?) RETURNING BALLID;", queriesVals)

        # Fetch list of returning ballIds
        # Need to get largest ballid and work back from there

        maxBallId = cur.execute("SELECT BALLID FROM Ball ORDER BY BALLID DESC LIMIT 1").fetchone()[0]
        ballIds = [(num, tableId) for num in range(startingBallId, maxBallId + 1)]

        cur.executemany("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", ballIds) 

        # Commit connection and close cursor
        self.conn.commit()
        cur.close()

        # Return tableId (in 0 index context)
        # ** TRY TO GET RID OF ARBITRARY ID OFFSETS
        return tableId 

    # Batchwise write table
    # This version also responsible for ShotTable entries
    def batchWriteTable(self, tables, shotId):
        # Get cursor
        cur = self.conn.cursor()

        # Get list of table times in tuple form
        tableTimes = [(table.time,) for table in tables]

        # Need to get starting tableId
        startingTableId = cur.execute("SELECT TABLEID FROM TTable ORDER BY TABLEID DESC LIMIT 1").fetchone()
        # If db is brand new we need to None check startingId
        if (startingTableId is None):
            startingTableId = 1
        else:
            startingTableId = startingTableId[0] + 1 


        # Now make new tables
        cur.executemany("INSERT INTO TTable (TIME) VALUES (?);", tableTimes) 

        # Same idea, get most recently created tableId
        maxTableId = cur.execute("SELECT TABLEID FROM TTable ORDER BY TABLEID DESC LIMIT 1").fetchone()[0]

        # Now make a LIST of all tableIds in LIST form (we can cast to tuple later)
        tableIds = [tableId for tableId in range(startingTableId, maxTableId + 1)]


        # Now for each table instance we just created in TTable REDACTED
        # Can't do executemany with tiered data, so we saved on about ~ (number of frames) queries
        # Update we can infact excecutemany by tactfully formatting our data
        # It's all about matching BALLIDs with TABLEIDs in BallTable
        # We can harvest ball params for free
        ballInsertVals = []

        # We need to be smarter with BallTable
        ballTableVals = []
        
        # Harvest initial ballId here
        startingBallId = cur.execute("SELECT BALLID FROM Ball ORDER BY BALLID DESC LIMIT 1").fetchone()

        # If db is brand new we need to None check startingId
        if (startingBallId is None):
            startingBallId = 1
        else:
            startingBallId = startingBallId[0] + 1

        # We'll also format our tableshot queries in this loop
        tableShotQueriesVals = []    

        for index, table in enumerate(tables):
            # As described
            tableShotQueriesVals.append((tableIds[index], shotId))

            # We will optimize by maintaining a list of queries and doing excecutemany
            queriesVals = []

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
                    queriesVals.append((ball.number, ball.pos.x, ball.pos.y, velX, velY))

                    # At this point we have a list of all balls for this specific tableId
                    ballInsertVals.append((ball.number, ball.pos.x, ball.pos.y, velX, velY)) 
                
            # The hard part is making BallTable match
            # Let's get how many balls our table has
            ballCount = table.ballCount()

            for num in range(startingBallId, startingBallId + ballCount):
                ballTableVals.append((num, tableIds[index]))
            
            # After doing all that, update the startingBallId
            startingBallId = startingBallId + ballCount

            

            # Commit connection and close cursor
            # Trying to slim down on commits
            #self.conn.commit()



        # We've collected all our ball value, actually send to db here
        cur.executemany("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?);", ballInsertVals)

        # Same for BallTable
        cur.executemany("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", ballTableVals) 


        # Batch is also responsible for TableShot table entries
        # We won't bother making batch tableshot function
        query = "INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?);"
        cur.executemany(query, tableShotQueriesVals)

        # Trying to slim down on commits
        #self.conn.commit()
        cur.close()

    # Get game method for game class
    def getGame(self, gameID):
        # Need cursor
        cur = self.conn.cursor()

        # Fetch game info from db
        query = """
                SELECT PLAYERID, PLAYERNAME, LOWBALLPLAYER, WINNER, WHOSTURNITIS
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

        # Return game name, and both players name. New addition, who has lowBalls, if game is finished and whos turn it is
        return data[0][1], data[1][1], data[0][2], data[0][3], data[0][4]

    # Set game method to create new game
    def setGame(self, player1Name, player2Name, whosTurnItIs):
        # Need cursor
        cur = self.conn.cursor()

        # Create game new game instance
        cur.execute("INSERT INTO Game (GAMENAME, LOWBALLPLAYER, WINNER, WHOSTURNITIS) VALUES (?, ?, ?, ?) RETURNING GAMEID;", ("placeholder", None, None, whosTurnItIs))

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
        # ** TRY TO GET RID OF ARBITRARY ID OFFSETS
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
        # ** TRY TO GET RID OF ARBITRARY ID OFFSETS
        cur.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (tableId, shotId)) 

        # Close and commit
        self.conn.commit()
        cur.close()

    # Method for finding latest table given a gameId
    def latestGameState(self, gameId):
        # Get cursor
        cur = self.conn.cursor()
        
        # Query for most recent state of table
        query = """
                SELECT TABLEID, PLAYERNAME
                FROM Shot
                JOIN TableShot on Shot.SHOTID = TableShot.SHOTID
                JOIN Player on Player.PLAYERID = Shot.PLAYERID
                WHERE Shot.GAMEID = ? 
                ORDER BY shot.SHOTID DESC, TABLEID DESC
                LIMIT 1 
                """

        data = cur.execute(query, (gameId,)).fetchone()

        if data is None:
            raise Exception("Our query for latest shot failed! This method as passed this ID: ", gameId)
        
        # Get latest table
        latestTable = self.readTable(data[0])

        # Need to find most recent player to shoot
        mostRecentPlayerName = data[1]
        
        # Want to find who's turn it is
        thisPlayersTurn = cur.execute("""SELECT PLAYERNAME 
                                         FROM Player 
                                         WHERE GAMEID = ? AND PLAYERNAME != ?
                                      """, (gameId, mostRecentPlayerName)).fetchone()[0]

        # Close connection off 
        cur.close()
        
        # Return most recent table and who's turn it is
        return latestTable, thisPlayersTurn

    def shotFrames(self, shotId):
        query = """
                SELECT TABLEID
                FROM TableShot
                WHERE SHOTID = ?
                ORDER BY TABLEID ASC
                """
        
        # Get cursor
        cur = self.conn.cursor()

        data = cur.execute(query, (shotId,)).fetchall()
        cur.close()

        # Return arrays of table
        return [tableId[0] for tableId in data] 

    
    # Close method
    def close(self):
        self.conn.commit()
        self.conn.close()


def getBallNumber(ball):
    if (isinstance(ball, StillBall)):
        return ball.obj.still_ball.number

    if (isinstance(ball, RollingBall)):
        return ball.obj.rolling_ball.number

    return None


"""
I know time complexity throws away any constants but I would like to do everything in one pass to be efficient
"""
def shotEventHandler(startTable, endTable, playerNumber, lowBallPlayer):
    ballSunk = None 
    winner = None
    lowBallsInPlay = None
    highBallsInPlay = None
    
    # 1. Check for sunken ball in segment
    for index, obj in enumerate(startTable):
        if (not (isinstance(obj, StillBall) or isinstance(obj, RollingBall))):
            continue
            
        # We can only have one ball sunk per call, so if we have none at index, that's the number
        number = getBallNumber(endTable[index])
        if (number is None):
            ballSunk = getBallNumber(obj)
            continue

        # Need to check for existence of low and high balls
        if (number <=7 and number > 0): 
            lowBallsInPlay = True

        if (number >= 9):
            highBallsInPlay = True

        # If we have a mismatch, we've sunk a ball
        if (obj != endTable[index]):
            ballSunk = getBallNumber(obj) 

    # Game status
    # If we didn't sink a ball, we have nothing left to do
    if (ballSunk is None):
        return ballSunk, lowBallPlayer, winner

    # Get other player number
    otherPlayerNumber = 1 if (playerNumber != 1) else 2 

    # Let's first check we don't have a winner/loser
    if (ballSunk == 8):
        # If we don't have a low ball player, whoever took the shot lost
        if (lowBallPlayer is not None):
            if (lowBallsInPlay is None and lowBallPlayer == playerNumber) or (highBallsInPlay is None and lowBallPlayer != playerNumber):
                winner = playerNumber
            else: 
                winner = otherPlayerNumber 
        else:
            winner = otherPlayerNumber

    # Now we've determined winners/losers. If we made it to this stage the only thing left to do is assign balls
    # If we dont have balls assigned to player, do so (we have ball sinking)
    if (lowBallPlayer is None and ballSunk != 0):
        lowBallPlayer = otherPlayerNumber if ballSunk >= 9 else playerNumber

    # We've determined: if a ball was sunk, if anyone has lowballs, if anyone won
    return ballSunk, lowBallPlayer, winner


class Game:
    def __init__( self, gameID=None, player1Name=None, player2Name=None):
        # Need a db instance to work with
        db = Database()

        # First constructor format
        if (gameID is not None and player1Name is None and player2Name is None):
            # For this constructor we know the gameID
            # ** TRY TO GET RID OF ARBITRARY ID OFFSETS
            self.gameID = gameID 

            # Get game data from db
            # Ridding ourselves of arbitrary ID shifting
            [p1, p2, lowBallPlayer, winner, whosTurnItIs] = db.getGame(gameID)

            # Populate attributes
            self.player1Name = p1
            self.player2Name = p2
            self.lowBallPlayer = lowBallPlayer 
            self.winner = winner
            self.whosTurnItIs = whosTurnItIs

            # Commit and close
            db.close()

        # Second constructor format
        elif (gameID is None and player1Name is not None and player2Name is not None):
            # Set attributes 
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.lowBallPlayer = None
            self.winner = None

            # Pick random person to go first
            if (random.choice([True, False])):
                self.whosTurnItIs = 1
            else:
                self.whosTurnItIs = 2
                

            # Put in db
            # Set unique game id attribute after creating it
            self.gameID = db.setGame(player1Name, player2Name, self.whosTurnItIs)

            # Commit and close
            db.close()

        # If neither are met, raise a type error
        else:
            # Commit and close
            db.close()
            
            raise TypeError

    # Update, we will create svgs as we create table frames to multiple/redudant trips to DB
    """
    Further update: we need to check frame by frame the status of the balls to officiate game
    Also need to make writeTables calls all at once too. This will be one major refactor
    """
    def shoot(self, table, xvel, yvel):
        # If table is None, we can't do anything
        if (table is None):
            return None

        # Get db instance
        db = Database()

        # Is this player 1 or player 2 shooting?
        playerName = self.player1Name if self.whosTurnItIs == 1 else self.player2Name

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


        # Tack on svg header
        svg = HEADER 

        # SHOOT REWRITE FOR OPTIMIZATION AND CHECKING STATUS OF TABLE WITH EVERY SEGMENT
        tablesToWrite = []

        # Lookahead flag for ballsunked
        cueBallSunk = None
        highBallSunk = None
        lowBallSunk = None

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
                # If we are we have some important things to consider
                # This is good rough in but will need to make function to decide where to set ball without collisions
                if (cueBallSunk):
                    startTable += StillBall(0, Coordinate(TABLE_WIDTH/2, TABLE_LENGTH - TABLE_WIDTH/2))
                
                tablesToWrite.append(startTable)
                svg = svg +  "<g class='hidden frame' >" + startTable.svg(False) + "</g>\n"
                break 

            # Need to compare/check for sunken balls
            ballSunk, lowBallPlayer, winner  = shotEventHandler(startTable, table, self.whosTurnItIs, self.lowBallPlayer)

            # If we sunk a cue ball we need to indicate to allow table to rerack
            if (ballSunk == 0):
                cueBallSunk = True

            # Before anything else I want to confirm any winner
            # Client side will stop all other activity and indicate winner
            if (winner is not None):
                # Also need to confirm such in db
                self.updateWinner(winner)

                name = self.player1Name if winner == 1 else self.player2Name
                svg = svg + f"<g class='hidden frame winner' > {name} Wins! </g>"
                
            # First thing is letting client know to assign balls
            if (self.lowBallPlayer is None and lowBallPlayer is not None):
                svg = svg + f"<g class='hidden frame lowBall' > {lowBallPlayer} </g>"

                # Also need to confirm such in db
                self.updateLowBallPlayer(lowBallPlayer)



            # If we sunk a ball, indicate as such within svg to client
            if (ballSunk is not None and ballSunk != 0):
                if (ballSunk < 8):
                    lowBallSunk = True
                
                if (ballSunk > 8):
                    highBallSunk = True
                
                svg = svg + f"<g class='hidden frame ballSunk' > {ballSunk} </g>"


            # Get time elapsed and number of frames
            frames = m.floor((table.time - startTime) / FRAME_INTERVAL)

            # Make a table for each frame in this segment of time
            for i in range(0, frames+1):
                # Get new table with roll applied
                newTable = startTable.roll(i * FRAME_INTERVAL)
              
                # Set its time correctly
                newTable.time = startTime + (i * FRAME_INTERVAL)

                # Append to list of tables to write to db
                tablesToWrite.append(newTable)


                # Tack svg frame onto reel
                svg = svg +  "<g class='hidden frame' >" + newTable.svg(False) + "</g>\n"

                # Provided roll function does not cast deaccelerating balls to still
                # Must include actual frame sent by C segment function
                if (i == frames and table.segment() is not None):
                    tablesToWrite.append(table)
                    svg = svg +  "<g class='hidden frame' >" + table.svg(False) + "</g>\n"

        # Do all writing to db here
        db.batchWriteTable(tablesToWrite, shotId)

        # Commit and close
        db.close()

        

        # Also need to determine who's turn it is next
        if (self.lowBallPlayer is not None):
            # Turns only change if player did not pot one of their balls
            if (self.lowBallPlayer == self.whosTurnItIs):
                if (lowBallSunk is None):
                    self.toggleTurn()
            else:
                if (highBallSunk is None):
                    self.toggleTurn()
        
        elif ballSunk == 0:
            self.toggleTurn()
        
        # Now let client know the news:
        svg = svg + "<g class='frame turnUpdate' >" + str(self.whosTurnItIs) + "</g>\n" 
        
        # Tack on footer
        svg = svg + FOOTER

        # Return shotId to make it easiest on server side
        # Update: return massive svg with frames as well
        return shotId, svg 

    # Need to update who's has what balls
    def updateLowBallPlayer(self, whoHasLowBalls):
        db = Database()
        cur = db.conn.cursor()

        # Update status of who's playing what balls
        query = """
                UPDATE Game 
                SET LOWBALLPLAYER = ? 
                WHERE GAMEID =  ?
                """ 

        # Excecute update
        cur.execute(query, (whoHasLowBalls, self.gameID))
        cur.close()
        db.close()

        # Make sure to update locally as well
        self.lowBallPlayer = whoHasLowBalls
    
    # Need to update who's has what balls
    def updateWinner(self, winner):
        db = Database()
        cur = db.conn.cursor()

        # Update status of who's playing what balls
        query = """
                UPDATE Game 
                SET WINNER = ? 
                WHERE GAMEID =  ?
                """ 

        # Excecute update
        cur.execute(query, (winner, self.gameID))
        cur.close()
        db.close()

        # Make sure to update locally as well
        self.winner = winner

    def toggleTurn(self):
        if (self.whosTurnItIs == 1):
            self.whosTurnItIs = 2
        
        else: 
            self.whosTurnItIs = 1
        
        db = Database()
        cur = db.conn.cursor()

        # Update status of who's playing what balls
        query = """
                UPDATE Game 
                SET WHOSTURNITIS = ? 
                WHERE GAMEID =  ?
                """ 

        # Excecute update
        cur.execute(query, (self.whosTurnItIs, self.gameID))
        cur.close()
        db.close()

    def getCurrentPlayer(self):
        if self.whosTurnItIs == 1:
            return self.player1Name
        return self.player2Name

    
