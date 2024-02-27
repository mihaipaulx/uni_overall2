var socket = io()

var prevDomain = "";

function toggleEvent() {
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

socket.on("spider_closed", function (data){
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
})
