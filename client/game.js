// Need to get organized before this one JS file becomes massive and messy

// CONSTANTS
const MAXVECTORLENGTH = 200
const MAXSPEED = 10000 // (mm/s)
const LOWBALLS = 
` 
<svg>
    <circle id="1" cx="10" cy="10" r="7" fill="YELLOW" />
    <circle id="2" cx="30" cy="10" r="7" fill="BLUE" />
    <circle id="3" cx="50" cy="10" r="7" fill="RED" />
    <circle id="4" cx="70" cy="10" r="7" fill="PURPLE" />
    <circle id="5" cx="90" cy="10" r="7" fill="ORANGE" />
    <circle id="6" cx="110" cy="10" r="7" fill="GREEN" />
    <circle id="7" cx="130" cy="10" r="7" fill="BROWN" />
    <circle id="8p1" cx="130" cy="10" r="7" fill="BLACK"></circle>
</svg>` 

const HIGHBALLS = 
`
<svg >
    <circle id="9" cx="10" cy="10" r="7" fill="LIGHTYELLOW" />
    <circle id="10" cx="30" cy="10" r="7" fill="LIGHTBLUE" />
    <circle id="11" cx="50" cy="10" r="7" fill="PINK" />
    <circle id="12" cx="70" cy="10" r="7" fill="MEDIUMPURPLE" />
    <circle id="13" cx="90" cy="10" r="7" fill="LIGHTSALMON" />
    <circle id="14" cx="110" cy="10" r="7" fill="LIGHTGREEN" />
    <circle id="15" cx="130" cy="10" r="7" fill="SANDYBROWN" />
    <circle id="8p2" cx="130" cy="10" r="7" fill="BLACK"></circle>
</svg>
`

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
            animate(response)
        },
        error: function(xhr, status, error) {
            console.error('Failed to shoot:', error);
        }
    });
}

const setWhosTurnItIs = () => {
    thisPlayersTurn =  parseInt($('#thisPlayersTurn').html())

    if (thisPlayersTurn === 1) {
        $('#leftTurn').removeClass("hidden")
        return
    }

    $('#rightTurn').removeClass("hidden")
}


const setWhosTurnItIsLive = (whosTurn) => {
    const leftTurn = $('#leftTurn')
    const rightTurn = $('#rightTurn')


    if (whosTurn === 1) {
        leftTurn.removeClass('hidden')
        rightTurn.addClass('hidden')
        return
    }

    rightTurn.removeClass('hidden')
    leftTurn.addClass('hidden')

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

const setLowBall = (playerNum) => {
    left = $('#leftBalls')
    right = $('#rightBalls')

    if (playerNum === 1){
        left.append(LOWBALLS)
        right.append(HIGHBALLS) 
        return
    }

    left.append(HIGHBALLS)
    right.append(LOWBALLS)
}






const animate = (svg) => {
    // Put svg into animation div
    $('#animation').empty().html(svg)
    toggleAnimationOn(true)

    // Get all the <g> elements with the class "frame"
    const frames = $('.frame');
    const frameCount = frames.length

    // I want to plug last frame of svg post into interactiveGame div
    const lastFrameContent = frames.eq(frameCount-2).html()
    const whosTurn = parseInt(frames.eq(frameCount-1).html())
    console.log(whosTurn)
    
    function showNextFrame(index) {
        // Get current frame just the once
        const currentFrame = frames.eq(index)

        // Hide the current frame (if any)
        if (index > 0) {
            frames.eq(index - 1).addClass('hidden');

            if (currentFrame.hasClass('lowBall') || 
                currentFrame.hasClass('ballSunk')){
                    frames.eq(index + 1).removeClass('hidden')
                }
        }
    
        // Show the next frame
        if (index < frameCount) {
            // We have to process info frames
            if (currentFrame.hasClass('lowBall')) {
                const num = parseInt(currentFrame.html())
                setLowBall(num)
                
                requestAnimationFrame(() => {
                    showNextFrame(index + 1);
                }); 
            } 

            else if (currentFrame.hasClass('ballSunk')) {
                const num = parseInt(currentFrame.html())

                // Remove ball from list for player 
                // May need to come back and delete 8 ball
                $(`#${num}`).remove()
                
                requestAnimationFrame(() => {
                    showNextFrame(index + 1);
                }); 
            }

            else {
                // requestAnimation Attempt
                currentFrame.removeClass('hidden')
                requestAnimationFrame(() => {
                    showNextFrame(index + 1);
                });
            }
            
            
            // Need special case for very last frame
            if (index === frameCount - 2) {
                // Put last frame into interactive div
                $('#insertFrameHere').empty().html(lastFrameContent);
                toggleAnimationOn(false)
                setWhosTurnItIsLive(whosTurn)
                refresh()
            }
        }
    }


    // Start the animation by showing the first frame
    showNextFrame(0);
}    



const attachEventHandlers = () => {
    // Get svg div
    const svgContainer = $('#interactiveGame')


    // PRE SHOT LOGIC
    // Now we can interact with the SVG elements
    // Let's get cueBall element so we can work with it
    cueBall = svgContainer.find("#cueBall")


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
    $(document).on('mousemove', function(event) {
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
    $(document).on('mouseup', function() {
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
}

const refresh = () => {
    attachEventHandlers()
}



$(document).ready(() => {
    attachEventHandlers()
    setWhosTurnItIs()
});


