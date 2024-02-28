window.addEventListener("DOMContentLoaded", e => {
    const socket = io();

    // Check if the socket is connected before executing further code
    socket.on("connect", function() {
        // This function will execute once the socket connection is successful
        console.log("Socket connected successfully!");

        socket.on("spider_closed", function(data) {
            console.log("SPIDER CLOSED RECEIVED");
            console.log(data);

            var ul = document.createElement("ul");

            // Loop through the items array and create list items for each item
            data.forEach(function(item) {
                var li = document.createElement("li"); // Create list item

                // Create anchor element
                var a = document.createElement("a");
                a.href = item.url; // Set href attribute
                a.textContent = item.url; // Set text content

                // Append Type and Link to the list item
                li.textContent = item.type + ": ";
                li.appendChild(a);

                // Append list item to the unordered list
                ul.appendChild(li);
            });

            // Get the container element where the list will be appended
            var container = document.getElementById("linkContainer");

            // Clear container content
            container.innerHTML = "";

            // Append the unordered list to the container element
            container.appendChild(ul);
        });
    });

    // Error handling for connection failure
    socket.on("connect_error", function(error) {
        console.error("Socket connection failed:", error);
    });

    socket.on("disconnect", function() {
        console.log("Socket disconnected.");
        // Handle disconnection here, such as displaying a message to the user or attempting to reconnect.
    });

    document.getElementById("submit-form").addEventListener("submit", function(e) {
        e.preventDefault()
        toggleEvent(socket);
    });

});

function toggleEvent(socket) {
    var prevDomain = "";
    var url = document.getElementById("textInput").value;
    try {
        var currentDomain = (new URL(url)).hostname.replace(/^www\./, '').split('.').slice(-2).join('.');
    } catch(e) {
        currentDomain = ""
    } finally {
        if (currentDomain !== "" && currentDomain !== prevDomain) {
            socket.emit('submit', currentDomain, url);
            console.log("submit");
            prevDomain = currentDomain
        }
    }
}