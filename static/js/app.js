document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    
    document.querySelector("#voteButton").onclick = function() {
        var vote = document.querySelector("#vote").value;
        if(vote) {
            socket.emit('castVote', {vote: vote});
        } else {
            alert("Please enter a vote.");
        }
    };

    socket.on('voteResponse', function(data) {
        if(data.success) {
            document.querySelector("#voteButton").style.color = "green";
            document.querySelectorAll(".featured-player").forEach(function(element) {
                element.style.borderColor = "green";
            });
            document.querySelectorAll(".featured-player").forEach(function(element) {
                element.style.backgroundColor = "lightgreen";
            });
            document.getElementById('voteButton').disabled = true;
            var message = "You voted for: " + data.voted_player;
            document.getElementById('voteResultMessage').innerText = message;
        } else {
            document.querySelector("#voteButton").style.color = "purple";
        }
    });

    socket.on('update_player_vote', (data) => {
        var voted_player = data.voted_player
        var voted_player_div = document.getElementById(voted_player);
        // Update the border color of the element when the 'update_player_vote' event is received
        if (voted_player_div) {
        console.log(voted_player)
        voted_player_div.style.borderColor = 'green';
        voted_player_div.style.backgroundColor = 'lightgreen'
        }
    });

    socket.on('update_village', function(data) {
        // Update webpage content
        document.getElementById('content').innerHTML = data.html
    });
});