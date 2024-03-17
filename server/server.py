import os # Check if file exists in directory
import re # Need regular expressions
import sys; # used to get argv
import math as m
import Physics as p
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, parse_qsl;
import random



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
 
    


# Helper function to delete files
def deleteTables():
    files = os.listdir('.')
    
    # Look for any table files and delete them
    for file in files:
        if re.match(r'^table-\w+\.svg$', file):
            os.remove('./' + file)



# Define routes 
routes = {
            '/': '../client/index.html',
            '/client/index.js': '../client/index.js',
            '/client/game.js': '../client/game.js'
        }

staticFiles = ['../client/index.html', '../client/index.js', "../client/game.js"]


# My own request handler (GETs and POSTs)
class PoolServer( BaseHTTPRequestHandler ):
    """
    GET Requests we need:
    - any static files (index.html, index.js etc)
    - new shot
    - game page
    """
    def do_GET(self):
        # Parse url
        parsedPath = urlparse(self.path).path;

        # We'll look for any of the existing server routes
        # check if the web-pages matches the list
        if parsedPath in routes and routes[parsedPath] in staticFiles:
            # Get actual path
            path = routes[parsedPath]   

            # Open file and pass back to client
            fp = open(path);
            content = fp.read();

            # Set headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(content));
            self.end_headers();

            # Send it to browser
            self.wfile.write(bytes(content, "utf-8"));

            # Close the file
            fp.close();

           
        elif parsedPath.startswith('/game/'):
            # Get game id from path (subject to change later)
            gameId = parsedPath.split('/')[-1]

            # TODO: Dynamically fetch and feed latest shot to client
            """ 
            Need to get most recent state of game, as well as who last shot
            Then serve page with interactable cue with that table state
            Then player will make post request for new shot
            and then we somehow (tbd) dynamically animate the screen.
            Once that finishes we are back to beginning. This way if the user refreshes,
            we can just return to most recent state of game
            """

            # Get latest game state from db
            db = p.Database()
            latestTable, thisPlayersTurn = db.latestGameState(gameId)


            # TODO: Check if game has been won/lost

            # Get html file and embed table svg
            # Read the HTML template file
            with open('../client/game.html', 'r') as file:
                gameHtml = file.read()

            # Replace the placeholder with table SVG
            tableSvg = latestTable.svg()
                
            response = gameHtml.format(svgContent=tableSvg)

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
            newGame = p.Game(None, "Game1", p1, p2)

            # Make brand new table with break setup
            table = newTable()

            # Put table in db
            # Also log a new shot in db (with vel of 0)
            # Will make it easier to fetch most current shot for given game id
            # Randomly pick p1 or p2, whoever is not picked will take first actual shot
            if (random.choice([True, False])):
                newGame.shoot("tbd", p1, table, 0, 0)
            else:
                newGame.shoot("tbd", p2, table, 0, 0)

            # Need to send gameId back to client for new game window
            response = str(newGame.gameID)
            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(response));
            self.end_headers();
        
            # Actually pass the id back
            self.wfile.write(bytes(response, "utf-8"))

        else:
            # generate 404 for POST requests that aren't any of the above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


# Main piece to instantiate server on port parsed from argv
if __name__ == "__main__":
    # Create server on port passed by argv
    httpd = HTTPServer(('0.0.0.0', 8080), PoolServer);

    # Let the console know the server is running at specified port
    print( "Server listing in port: 8080 TEST");

    # Run server indefinetely (Terminate by stopping terminal session)
    httpd.serve_forever();
