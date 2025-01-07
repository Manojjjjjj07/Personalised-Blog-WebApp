function react(postId, reactionType) {
    fetch(`/post/${postId}/react/${reactionType}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
        }
    })
    .then(response => response.json()) // Parse the JSON response
    .then(data => {
        // Check if an error exists in the response
        if (data.error) {
            alert(data.error); // Display error message to the user
        } else {
            // Dynamically update the reaction counts on the page
            document.querySelector(`button[onclick="react('${postId}', 'like')"]`).innerHTML = `👍 Like (${data.reaction_count.like || 0})`;
            document.querySelector(`button[onclick="react('${postId}', 'love')"]`).innerHTML = `❤️ Love (${data.reaction_count.love || 0})`;
            document.querySelector(`button[onclick="react('${postId}', 'clap')"]`).innerHTML = `👏 Clap (${data.reaction_count.clap || 0})`;
        }
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie matches the requested name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
