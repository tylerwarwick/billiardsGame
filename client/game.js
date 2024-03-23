// Need to get organized before this one JS file becomes massive and messy

// CONSTANTS
const MAXVECTORLENGTH = 200
const MAXSPEED = 10000 // (mm/s)


// STATE ElEMENTS
let shotInterval = {
    start:  null,
    end: null,
}

// MATH FUNCTIONS
// Define function that determines the max length of vector on screen
const length = (x, y) => {
    return Math.sqrt((x*x) + (y*y))
}

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
    return [xUnit * speed, yUnit * speed]
}

// REQUESTS
// Shoot POST request
const shoot = (xVel, yVel) => {
    // Will need to refetch latest game state from gameID on server side
    // Unless I can somehow maintain tableId somewhere
    // We'll stick with the former for now

    // Get gameID from address
    const url = (window.location.pathname).split('/')
    const gameId = url[url.indexOf("game") + 1]    

    const JSONData = JSON.stringify(
    {
        gameId : gameId,
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
            //stringArr = response.split('-')
            //console.log(parseInt(stringArr[0]))
            //animate(parseInt(stringArr[0]), parseInt(stringArr[1]))
            animate(response)
        },
        error: function(xhr, status, error) {
            console.error('Failed to shoot:', error);
        }
    });
}


const getFrame = (tableId) => {
    // Need to wrap as promise
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `/table/${tableId}`,
            method: 'GET',
            contentType: 'application/json',
            success: (response) => {
                return resolve(response)
            },
            error: (response) => {
                reject(response)
            }
        })
    }) 
}


const toggleAnimationOn = (bool) => {
    const gameDiv = $('#interactiveGame')
    const animationDiv = $('#animation')

    if (bool){
        gameDiv.addClass("hidden")
        animationDiv.removeClass("hidden")
    }
    else {
        gameDiv.removeClass("hidden")
        animationDiv.addClass("hidden")
        animationDiv.empty()
    }
}

const animate = (svg) => {
    // Put svg into animation div
    $('#animation').empty().html(svg)
    toggleAnimationOn(true)

    // Get all the <g> elements with the class "frame"
    const frames = $('.frame');
    const frameCount = frames.length

    
    function showNextFrame(index) {
        // Hide the current frame (if any)
        if (index > 0) {
            frames.eq(index - 1).addClass('hidden');
        }
    
        // Show the next frame
        if (index < frameCount) {
            /*
            // delay().queue() attempt
            frames.eq(index).removeClass('hidden').delay(40).queue((next) => {
                showNextFrame(index + 1);
                next();
            });
            */

            
            // requestAnimation Attempt
            frames.eq(index).removeClass('hidden')
            requestAnimationFrame(() => {
                showNextFrame(index + 1);
            });
            
            
            /*
            // setTimeout attempt
            frames.eq(index).removeClass('hidden')
            setTimeout(() => {
                showNextFrame(index+1)
            }, 40)
            */

            // Need special case for very last frame
            if (index === frameCount - 1) {
                // Put last frame into interactive div
                $('#interactiveGame').empty().html("NEXT SHOT");
            }
        }
    }


    // Start the animation by showing the first frame
    showNextFrame(0);

    // Go back to interactive display
    //toggleAnimationOn(false)
}    


/*
const animate = (start, end) => {
    // Need to request table from server over interval of IDs and cast to screen
    let i = start
    
    toggleAnimationOn(true)    
    
    while (i<= end){
        getFrame(i)
        .then((response) => {
            $('#animation').empty()
            setTimeout(() => { $('#animation').html(response)}, 40)
            
        })
        .catch((error) => {
            console.log("Broken frame retrieval")
        })
        i++
    }   
    
    $('#interactiveGame').empty()
    $('#interactiveGame').html()
    

    const animateFrame = () => {
        if (i <= end) {
            getFrame(i)
                .then((response) => {
                    $('#animation').html(response);
                    i++;
                    requestAnimationFrame(animateFrame); // Request the next frame
                })
                .catch((error) => {
                    console.log("Broken frame retrieval");
                });
        } else {
            toggleAnimationOn(false); // Animation complete
        }
    };

    animateFrame(); // Start the animation loop
}

*/

// Main interaction Jquery block
$(document).ready(function(){
        // Get svg div
        const svgContainer = $('#interactiveGame')


        // PRE SHOT LOGIC
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
                const [xVel, yVel] = getUsableVelocities(xVec, yVec)

                // Invert values to put in context of pool table
                shoot(-xVel, -yVel)

                // Reset colour of cue ball
                cueBall.attr("fill", "white") 

                // Get rid of the line again
                removeVector()
            } 
            isDragging = false;
            
        })


        // POST SHOT (ANIMATION) LOGIC
        






});
