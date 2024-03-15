// Define function that determines the max length of vector on screen
const length = (x, y) => {
    return Math.sqrt((x*x) + (y*y))
}


// Take angle and output vector of fixed length
const maxVector = (x1, y1, x2, y2) => {
    // Get length
    const len = length(x2-x1, y2-y1)

    if (len == 0) return [0, 0]

    return [x2-x1, y2-y1]

    // If within allotted range, return unchanged offset
    if (len < 500){
        return [x2-x1, y2-y1]
    }

    // Otherwise shorten magnitude while maintaining angle (unit vector) 
    return [500*(x2-x1)/len, 500*(y2-y1)/len]

}

// Load svg content in
// This is the only way that works cross browser
// SVG behaviour is not well defined currently
$.ajax({
    url: 'table0120.svg',
    dataType: 'xml',
    success: (svgData) => {
        svgContent = $(svgData.documentElement)

        // Get div where we will insert svg content
        const svgContainer = $('#svgContainer')

        // Insert the SVG content into the container
        svgContainer.append(svgContent);
        
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

        function updateVector(newX, newY){
            if (vector){
                vector.attr("x2", newX)
                vector.attr("y2", newY)
            }
            else console.log("Vector not defined!")
           
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

        $(document).on('mousemove', function(event) {
            // Check if dragging is in progress
            if (isDragging) {
                // Tell the console what our vector components look like
                console.log('Dragging... from: ', mouseX, " ", mouseY);
                console.log("to: ", event.clientX, "  ", event.clientY) 

                const delta = maxVector(mouseX, event.clientX, mouseY, event.clientY)

                // Can circle back with extra time to change mouseX and mouseY
                // So no clipping occurs with vector and cue ball
                makeVector(mouseX, mouseY, mouseX+delta[0], mouseY+delta[1])
            }

          });

        // Event listener for mouse up
        $(document).on('mouseup', function() {
            // Set the flag to false when mouse button is released
            if (isDragging){
                cueBall.attr("fill", "white") 
                removeVector()
            } 
            isDragging = false;
            
        })
    },
    error: function(xhr, status, error) {
        console.error("Failed to load SVG:", error);
    }
});
