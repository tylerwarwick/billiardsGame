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

        // Get the dimensions of the SVG container
        const svgContainerWidth = svgContainer.width();
        const svgContainerHeight = svgContainer.height();

        // Calculate the position of the SVG container relative to the viewport
        const svgContainerLeft = (windowWidth - svgContainerWidth) / 2;
        const svgContainerTop = (windowHeight - svgContainerHeight) / 2;


        // Gonna define line creator function here
        const vector = $("#vector")
        function makeVector(x1, y1, x2, y2) {
            // Create a new line element
            /*
            let line = $('<line/>', {
                id: 'vector',
                x1: x1,
                y1: y1,
                x2: x2,
                y2: y2,
                'stroke-width': '28',
                stroke: 'black',
                style: 'z-index: 9999;'
            })
   
            // Append the line to the SVG container
            svgContent.append(line);

            // Define pointer to actual line element in DOM
            vector = $('#vector')[0]; // Convert jQuery object to DOM element
            */
            
            vector.removeClass("hidden")
            vector.attr("x1", x1)
            vector.attr("y1", y1)
            vector.attr("x2", x2)
            vector.attr("y2", y2)
            console.log(svgContainerWidth)
            
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
 
                makeVector(mouseX, mouseY, event.clientX, event.clientY)
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
