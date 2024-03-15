/* 
We will be doing one page game
Given the constraint of httpServer, dynamically changing page content 
makes the most sense (as opposed to redirects)
*/ 

// Handle home page new game creation
$(document).ready(function() {
    $('#playerForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        // Serialize form data
        const formData = $(this).serialize(); 
        console.log(formData)

        // Send form data to server using AJAX
        $.ajax({
            url: '/newGame',
            method: 'POST',
            contentType: 'application/json',
            data: formData,
            success: function(response) {
                console.log('New game created successfully');
                // Redirect to the new page or handle response as needed
            },
            error: function(xhr, status, error) {
                console.error('Failed to create new game:', error);
                // Handle error response from the server
            }
        });
    });
});
