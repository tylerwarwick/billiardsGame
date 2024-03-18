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
       
        // Send form data to server using AJAX
        $.ajax({
            url: '/newGame',
            method: 'POST',
            contentType: 'application/json',
            data: formData,
            success: function(response) {
                // Move into game session
                window.location.replace(`/game/${parseInt(response)}`)
            },
            error: function(xhr, status, error) {
                console.error('Failed to create new game:', error);

                // Handle error response from the server
                alert("Something went wrong! Please try starting a game again")
            }
        });
    });
});
