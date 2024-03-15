import os # Check if file exists in directory
import re # Need regular expressions
import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future

import math as m # Need math and physics for table construction
import Physics as p


# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# Define routes 
routes = {
            '/': '../client/index.html'
        }


# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;


# Helper function to delete files
def deleteTables():
    files = os.listdir('.')
    
    # Look for any table files and delete them
    for file in files:
        if re.match(r'^table-\w+\.svg$', file):
            os.remove('./' + file)


# My own request handler (GETs and POSTs)
class PoolServer( BaseHTTPRequestHandler ):
    # Handle GET requests
    """
    GET Requests we need:
    - newShot
    """
    def do_GET(self):
        # Parse url
        parsed  = urlparse( self.path );

        # We'll look for any of the existing server routes
        # check if the web-pages matches the list
        if parsed.path in routes:

            path = routes[parsed.path]

            # Get HTML file
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
        
        # Look for table SVG files in this directory
        # Need regex or else client could request any file from server directory
        elif os.path.exists("." + parsed.path) and re.match(r'^/table-\w+\.svg$', parsed.path):


            # Get SVG file (rb mode for these)
            fp = open( '../client'+self.path, 'rb');
            content = fp.read();

            # Send response
            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # Write file 
            self.wfile.write(content) 

            # Close the file
            fp.close();

        # If the path doesn't match any routes, send back 404
        else:
            # Send 404 response code
            self.send_response(404);

            # Close headers
            self.end_headers();

            # Write error message to screen
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

    # Handle POST request
    def do_POST(self):
        # Parse url as object to get path and form data
        parsed  = urlparse( self.path );

        if parsed.path in ['/display.html']:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   );
                            

            # Need to check that form data is valid
            # If any field is empty or not a float
            # Make list of required fields and their types
            required_fields = {
                'sb_number': int,
                'sb_x': float,
                'sb_y': float,
                'rb_number': int,
                'rb_x': float,
                'rb_y': float,
                'rb_dx': float,
                'rb_dy': float
            }

            # Check if each value is non-empty and the correct type
            for field, fieldType in required_fields.items():
               
                try:
                    # Check for non-empty status
                    form.getvalue(field).strip()

                    # Check for proper types
                    fieldType(form.getvalue(field).strip())
    
                except:
                    # If this occurs send 404 status back
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(bytes("404: Improper input", "utf-8"))

                    # Leave funtion excecution if this occurs
                    # Without this line, http complains about other status codes being sent
                    return
                
                
                    

            # Purge all old table SVGs
            deleteTables()
            
            
            # Create balls and table from form data
            # Create still ball                      
            sb = p.StillBall(
                                int(form.getvalue('sb_number').strip()), 
                                p.Coordinate(
                                    float(form.getvalue('sb_x').strip()),
                                    float(form.getvalue('sb_y').strip())
                                    )
                                  )

            # Create rolling ball
            # Need to calculate acceleration first
            # Store velocities
            xVel = float(form.getvalue('rb_dx').strip())
            yVel = float(form.getvalue('rb_dy').strip())

            # Get vector magnitude for speed
            speed = m.sqrt((xVel * xVel) + (yVel * yVel))

            # Calculate acclerations
            xAcc = (-xVel / speed) * p.DRAG
            yAcc = (-yVel / speed) * p.DRAG
            
            # Instantiate rolling ball
            rb = p.RollingBall(
                                int(form.getvalue('rb_number').strip()),
                                p.Coordinate(
                                    float(form.getvalue('rb_x').strip()),
                                    float(form.getvalue('rb_y').strip())
                                ), 
                                p.Coordinate(
                                    xVel,
                                    yVel
                                ), 
                                p.Coordinate(
                                    xAcc,
                                    yAcc
                                )
                )


            # Create table
            table = p.Table()

            # Add balls to table
            table += sb
            table += rb
            
            # Call segment and make svg for each milestone
            # Need to declare iterator
            num = 0
            
            # Going to declare html string first
            # So that we may append svg img tags with each new creation
            content = """<html>
                            <head>
                                <title> Display </title>
                                <script src="https://cdn.tailwindcss.com"></script>
                            </head>
                            <body>
                                <!-- Navbar -->
                                <nav class="bg-white fixed w-full z-20 top-0 start-0 border-b border-gray-200">
                                    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
                                        <button class="relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-purple-500 to-pink-500 group-hover:from-purple-500 group-hover:to-pink-500 hover:text-white focus:ring-4 focus:outline-none focus:ring-purple-200">
                                            <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white  rounded-md group-hover:bg-opacity-0">
                                                <a href="/shoot.html">Back to Shoot Page</a>
                                            </span>
                                        </button>
                                    </div>
                                </nav>
                                <!-- Main SVG's -->
                                <div class="bg-white w-full h-auto flex flex-col items-center justify-center pt-36 space-y-10 pb-36"> \n"""
            
            #<img src="/table-0.svg" alt="SERVER ERROR">
            while(table):
                
                with open(f'table-{num}.svg', 'w') as file:
                    # Create file
                    file.write(table.svg())

                    # Append to HTML string
                    content += f'<div class="w-1/3 h-1/3 space-y-6 flex justify-center items-center flex-col"><span class="bg-purple-100 text-purple-800 text-s font-medium me-2 px-5 py-1 rounded border border-2 border-purple-400">Snapshot {num+1}</span><img class="h-1/3 w-1/2" src="/table-{num}.svg" alt="SERVER ERROR"></div> \n'

                    # Increment iterator
                    num += 1

                # Run segment
                table = table.segment()

            # Slap the closing tags on there
            content += """</div></body></html>"""

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(content) );
            self.end_headers();

            # send it to the browser
            self.wfile.write(bytes(content, "utf-8"));
            
        elif parsed.path == "/newGame":
            print("POSTED")
              # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", 5 );
            self.end_headers();
            self.wfile.write(("Hello").encode('utf-8'))

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


# Main piece to instantiate server on port parsed from argv
if __name__ == "__main__":
    # Create server on port passed by argv
    httpd = HTTPServer(('localhost', int(sys.argv[1])), PoolServer);

    # Let the console know the server is running at specified port
    print( "Server listing in port:  ", int(sys.argv[1]));

    # Run server indefinetely (Terminate by stopping terminal session)
    httpd.serve_forever();
