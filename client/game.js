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
    if (len < 200){
        return [x2-x1, y2-y1]
    }

    // Otherwise shorten magnitude while maintaining angle (unit vector) 
    return [200*(x2-x1)/len, 200*(y2-y1)/len]

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

        $(this).on('mousemove', function(event) {
            // Check if dragging is in progress
            if (isDragging) {
                // Tell the console what our vector components look like
                console.log('Dragging... from: ', mouseX, " ", mouseY);
                console.log("to: ", event.clientX, "  ", event.clientY) 

                const [deltaX, deltaY] = maxVector(mouseX, mouseY, event.clientX, event.clientY)

                console.log("x displacement: ", event.clientX - mouseX)
                console.log("Calc delta: ", deltaX)
                // Can circle back with extra time to change mouseX and mouseY
                // So no clipping occurs with vector and cue ball
                makeVector(mouseX, mouseY, mouseX+deltaX, mouseY+deltaY)   
            }

          });

        // Event listener for mouse up
        $(this).on('mouseup', function() {
            // Set the flag to false when mouse button is released
            if (isDragging){
                cueBall.attr("fill", "white") 
                removeVector()
            } 
            isDragging = false;
            
        })
});
