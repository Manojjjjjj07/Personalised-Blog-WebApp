function react(postId, reactionType) {
    fetch(`/post/${postId}/react/${reactionType}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
        }
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector(`button[onclick="react('${postId}', 'like')"]`).innerHTML = `👍 Like (${data.likes})`;
        document.querySelector(`button[onclick="react('${postId}', 'love')"]`).innerHTML = `❤️ Love (${data.loves})`;
        document.querySelector(`button[onclick="react('${postId}', 'clap')"]`).innerHTML = `👏 Clap (${data.claps})`;
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
