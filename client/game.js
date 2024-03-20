// Define function that determines the max length of vector on screen
const length = (x, y) => {
    return Math.sqrt((x*x) + (y*y))
}

// Declare consts if we choose to change later
const MAXVECTORLENGTH = 200
const MAXSPEED = 10000 // (mm/s)


// Take angle and output vector of fixed length
const maxVector = (x1, y1, x2, y2) => {
    // Get length
    const len = length(x2-x1, y2-y1)

    if (len == 0) return [0, 0]

    // If within allotted range, return unchanged offset
    if (len < MAXVECTORLENGTH){
        return [x2-x1, y2-y1]
    }

    // Otherwise shorten magnitude while maintaining angle (unit vector) 
    return [MAXVECTORLENGTH*(x2-x1)/len, MAXVECTORLENGTH*(y2-y1)/len]

}

// Need to convert viewport grid vector to velocities for our shoot function server side
const getUsableVelocities = (xVec, yVec) => {
    // Get magnitude for vector components
    vecMagnitude = length(xVec, yVec)

    // Need unit vector components as well
    xUnit = xVec / vecMagnitude
    yUnit = yVec / vecMagnitude

    // Now get overall speed of velocity applied to ball
    // vecMagnitude over max vector length gives us our percentage of max speed
    speed = (vecMagnitude / MAXVECTORLENGTH) * MAXSPEED

    // Return x and y components of velocity
    return xUnit * speed, yUnit * speed
}

// Helper function for shoot post request
const shoot = (xVel, yVel) => {
    // Will need to refetch latest game state from gameID on server side
    // Unless I can somehow maintain tableId somewhere
    // We'll stick with the former for now

    const JSONData = JSON.stringify(
    {
        xVel : xVel,
        yVel : yVel
    })

    $.ajax({
        url: '/shoot',
        method: 'POST',
        contentType: 'application/json',
        data: JSONData,
        success: function(response) {
            // On success, animate
            console.log("Worked")
        },
        error: function(xhr, status, error) {
            console.error('Failed to shoot:', error);
        }
    });
}




$(document).ready(function(){
        // Get svg div
        const svgContainer = $('#svgContainer')

        // Now we can interact with the SVG elements
        // Let's get cueBall element so we can work with it
        const cueBall = svgContainer.find("#cueBall")

        // Define hover behaviour
        // When hovering, indicate as such
        cueBall.on("mouseenter", function() {
            $(this).attr("fill", "#E0E0E0")
        })
        
        cueBall.on('mouseout', function() {
            if (!isDragging) $(this).attr("fill", "white")
        })

        //Need to normlize coords in context of svg table
        // Get the position of the SVG container relative to the viewport
        const rect = svgContainer[0].getBoundingClientRect()


        // Get the dimensions of the window
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        

        // Gonna define line creator function here
        const vector = $("#vector")
        function makeVector(x1, y1, x2, y2) {
            vector.removeClass("hidden")
            vector.attr("x1", x1)
            vector.attr("y1", y1)
            vector.attr("x2", x2)
            vector.attr("y2", y2)
        }


        function removeVector(){
            vector.addClass("hidden")
        }

        // Now what happens when we click on it
        let isDragging = false;
        let mouseX, mouseY
        cueBall.on('mousedown', function(event) {
            isDragging = true

            // Let user know they are contacting it:
            $(this).attr("fill", "#E0E0E0")

            // Get the cursor position relative to the viewport
            mouseX = event.clientX;
            mouseY = event.clientY;
        })

        //Need a vector temp to pull velocity values from when mouse is let go of
        let xVec, yVec
        $(this).on('mousemove', function(event) {
            // Check if dragging is in progress
            if (isDragging) {
                // Get normalized vector
                const [deltaX, deltaY] = maxVector(mouseX, mouseY, event.clientX, event.clientY)
                
                // Track vector for use when mouse is lifted
                xVec = deltaX
                yVec = deltaY 

                // Can circle back with extra time to change mouseX and mouseY
                // So no clipping occurs with vector and cue ball
                makeVector(mouseX, mouseY, mouseX+deltaX, mouseY+deltaY)   
            }

          });

        // Event listener for mouse up
        $(this).on('mouseup', function() {
            // Set the flag to false when mouse button is released
            if (isDragging){
                // We'll make POST request first
                // We have vector components already at our disposal
                shoot(getUsableVelocities(xVec, yVec))

                // Reset colour of cue ball
                cueBall.attr("fill", "white") 

                // Get rid of the line again
                removeVector()
            } 
            isDragging = false;
            
        })

});
