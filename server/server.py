import json
import os # Check if file exists in directory
import re # Need regular expressions
import math as m
import Physics as p
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, parse_qsl;
import random

# Need to make function to format table svgs into format we can animate
def animationSvg(tableIds):
    str = ""

    db = p.Database() 

    for tableId in tableIds:
        str = str + "<g>" + db.readTable(tableId).svg(False) + "</g>"   

    db.close() 

    return str

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
 
    

# Holding onto my svg content here for a minute
lowBalls = [
"""<circle id="1" cx="10" cy="10" r="7" fill="YELLOW" />""",
"""<circle id="2" cx="30" cy="10" r="7" fill="BLUE" />""",
"""<circle id="3" cx="50" cy="10" r="7" fill="RED" />""",
"""<circle id="4" cx="70" cy="10" r="7" fill="PURPLE" />""",
"""<circle id="5" cx="90" cy="10" r="7" fill="ORANGE" />""",
"""<circle id="6" cx="110" cy="10" r="7" fill="GREEN" />""",
"""<circle id="7" cx="130" cy="10" r="7" fill="BROWN" />""",
"""<circle id="8p1" cx="130" cy="10" r="7" fill="BLACK"></circle>"""        
]


highBalls = [
"""<circle id="9" cx="10" cy="10" r="7" fill="LIGHTYELLOW" />""", 
"""<circle id="10" cx="30" cy="10" r="7" fill="LIGHTBLUE" />""",
"""<circle id="11" cx="50" cy="10" r="7" fill="PINK" />""",
"""<circle id="12" cx="70" cy="10" r="7" fill="MEDIUMPURPLE" />""",
"""<circle id="13" cx="90" cy="10" r="7" fill="LIGHTSALMON" />""",
""" <circle id="14" cx="110" cy="10" r="7" fill="LIGHTGREEN" />""",
""" <circle id="15" cx="130" cy="10" r="7" fill="SANDYBROWN" />""",
"""<circle id="8p2" cx="130" cy="10" r="7" fill="BLACK"></circle>"""
]



# Define routes 
routes = {
            '/': '../client/index.html',
            '/client/index.js': '../client/index.js',
            '/client/game.js': '../client/game.js',
            '/client/images/ash.png': '../client/images/ash.png',
            '/client/images/gary.png': '../client/images/gary.png',
        }

staticFiles = ['../client/index.html', '../client/index.js', "../client/game.js", "../client/images/ash.png", "../client/images/gary.png"]


# My own request handler (GETs and POSTs)
class PoolServer( BaseHTTPRequestHandler ):
    """
    GET Requests we need:
    - any static files (index.html, index.js etc)
    - new shot
    - game page
    """
    # TODO: Dynamically fetch and feed latest shot to client
    """ 
    Need to get most recent state of game, as well as who last shot
    Then serve page with interactable cue with that table state (GET /game/id)

    Then player will make post request for new shot (POST shoot)
    and then we somehow (tbd) dynamically animate the screen (on POST success GET animation frames)

    Once that finishes we are back to beginning. This way if the user refreshes,
    we can just return to most recent state of game (No action required, hide animation frame leaving next shot page exposed)
    """   

    def do_GET(self):
        # Parse url
        parsedPath = urlparse(self.path).path;

        # We'll look for any of the existing server routes
        # check if the web-pages matches the list
        if parsedPath in routes and routes[parsedPath] in staticFiles:
            # Get actual path
            path = routes[parsedPath]   

            # Check if the requested file is a PNG
            if path.endswith('.png'):
                content_type = 'image/png'
            else:
                content_type = 'text/html'

            # Open file and pass back to client
            fp = open(path, 'rb');
            content = fp.read();

            # Set headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", content_type );
            self.send_header( "Content-length", len(content));
            self.end_headers();

            # Send it to browser
            self.wfile.write(content);

            # Close the file
            fp.close();

            
        elif parsedPath.startswith('/game/'):
            # Get game id from path (subject to change later)
            gameId = parsedPath.split('/')[-1]

            # Get latest game state from db
            db = p.Database()
            latestTable, thisPlayersTurn = db.latestGameState(gameId)
            db.close()

            # I need both players name
            game = p.Game(gameId)

            # TODO: Check if game has been won/lost
            # Will need to do here as well as make into own endpoint for client to call after every shot

            # Get html file and embed table svg
            # Read the HTML template file
            with open('../client/game.html', 'r') as file:
                gameHtml = file.read()

            # Replace the placeholder with table SVG
            tableSvg = latestTable.svg(False)

            player1Balls = ""
            player2Balls = ""


            # Get ball svg contents
            if (game.lowBallPlayer is not None):
                lowBallContent = ""
                highBallContent = ""
                lowBallNums, HighBallNums = latestTable.lowAndHighBalls()

                lowBallContent = lowBallContent + "<svg>"
                highBallContent = highBallContent + "<svg>"

                for num in lowBallNums:
                    lowBallContent = lowBallContent + lowBalls[num-1]
                
                for num in HighBallNums:
                    highBallContent = highBallContent + highBalls[num-9]

                lowBallContent = lowBallContent + lowBalls[7] + "</svg>"
                highBallContent = highBallContent + highBalls[7] + "</svg>"

                if (game.lowBallPlayer == 1):
                    player1Balls = lowBallContent 
                    player2Balls = highBallContent
                else:
                    player1Balls = highBallContent
                    player2Balls = lowBallContent

            winner = ""
            if (game.winner is not None):
                winner = str(game.getCurrentPlayer()) + " Wins!"

            response = gameHtml.format(svgContent=tableSvg, 
                                       p1Name = game.player1Name, 
                                       p2Name = game.player2Name, 
                                       whosTurnItIs = game.whosTurnItIs,
                                       player1Balls = player1Balls,
                                       player2Balls = player2Balls,
                                       winner = winner 
                                       )

            # Set headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(response));
            self.end_headers();

            # Write the HTML response with embedded SVG content
            self.wfile.write(response.encode('utf-8'))    

        # If the path doesn't match any routes, send back 404
        else:
            # Send 404 response code
            self.send_response(404);

            # Close headers
            self.end_headers();

            # Write error message to screen
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"));



    # Handle POST request
    def do_POST(self):
        # Parse url as object to get path and form data
        path = urlparse(self.path).path;

        # Handle creation of new game
        if path == "/newGame":
            # Get data from request
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            # convert POST content into a dictionary
            data = parse_qs(body.decode( 'utf-8' ));

            # Get player names 
            p1 = data["player1"][0]
            p2 = data["player2"][0]
            

            # Make a new game with game class
            # Game is automatically written to db with init
            newGame = p.Game(None, p1, p2)

            # Make brand new table with break setup
            table = newTable()

            # REDACTED: We not maintain whos turn it is in db 
            # Put table in db
            # Also log a new shot in db (with vel of 0)
            # Will make it easier to fetch most current shot for given game id
            # Randomly pick p1 or p2, whoever is not picked will take first actual shot

            newGame.shoot(table, 0.0, 0.0)

            # Need to send gameId back to client for new game window
            response = str(newGame.gameID)

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(response));
            self.end_headers();
        
            # Actually pass the id back
            self.wfile.write(bytes(response, "utf-8"))

            """
            When the client calls shoots I am going to pass back the required in between frames.
            Rather than passing an id or timestamps for which they can then make a GET request with.
            I think this will make more sense. UPDATE: we are passing back interval of ids in which they can make get requests.
            """
        elif path == '/shoot':
            # Get data from request
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            # Get velocity values from request
            data = json.loads(body.decode("utf-8")); 

            xVel = float(data["xVel"])
            yVel = float(data["yVel"])

            # Also need to parse gameID from request
            gameId = int(data["gameId"])

            # Fetch latest game state
            db = p.Database()
            latestTable, thisPlayersTurn = db.latestGameState(gameId) 
                        
            # Get game object
            game = p.Game(gameId)

            # Shoot with velocities from client
            shotId, svg = game.shoot(latestTable, xVel, yVel)
            response = svg

            # Close db
            db.close()

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(response));
            self.end_headers();
         
            self.wfile.write(bytes(response, "utf-8"))

        else:
            # generate 404 for POST requests that aren't any of the above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


# Main piece to instantiate server on port parsed from argv
if __name__ == "__main__":
    # Create server on port passed by argv
    httpd = HTTPServer(('0.0.0.0', 50124), PoolServer);

    # Let the console know the server is running at specified port
    print( "Server listing in port: 50124");

    # Run server indefinetely (Terminate by stopping terminal session)
    httpd.serve_forever();
