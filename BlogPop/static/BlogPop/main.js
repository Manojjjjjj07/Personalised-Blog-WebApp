function react(postId, reactionType) {
    fetch(`/post/${postId}/react/${reactionType}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Add CSRF token to headers
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        // Check if an error exists in the response
        if (data.error) {
            alert(data.error); // Display error message to the user
        } else {
            // Dynamically update the reaction counts on the page
            updateReactionCounts(postId, data.reaction_count);
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateReactionCounts(postId, reactionCounts) {
    const likeButton = document.querySelector(`button[onclick="react('${postId}', 'like')"]`);
    const loveButton = document.querySelector(`button[onclick="react('${postId}', 'love')"]`);
    const clapButton = document.querySelector(`button[onclick="react('${postId}', 'clap')"]`);

    if (likeButton) {
        likeButton.innerHTML = `👍 Like (${reactionCounts.like || 0})`;
    }
    if (loveButton) {
        loveButton.innerHTML = `❤️ Love (${reactionCounts.love || 0})`;
    }
    if (clapButton) {
        clapButton.innerHTML = `👏 Clap (${reactionCounts.clap || 0})`;
    }
}

// Helper function to retrieve the CSRF token from cookies
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


function toggleSearchBar() {
    const searchBar = document.getElementById('search-bar');
    if (searchBar.style.display === 'none') {
        searchBar.style.display = 'block';
    } else {
        searchBar.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('search-btn');
    if (searchButton) {
        searchButton.addEventListener('click', searchPosts);
    }
});

function searchPosts() {
    const query = document.getElementById('search-input').value;
    fetch(`/search-posts/?q=${encodeURIComponent(query)}`)
        .then((response) => response.json())
        .then((data) => {
            const postsContainer = document.getElementById('posts-container');
            postsContainer.innerHTML = ''; // Clear old search results

            if (data.results.length > 0) {
                data.results.forEach((post) => {
                    const postElement = document.createElement('div');
                    postElement.innerHTML = `
                        <h3><a href="${post.url}">${post.title}</a></h3>
                        <p>${post.highlighted_content}</p>
                        <p><small>${post.date_posted} by ${post.author.username}</small></p>
                    `;
                    postsContainer.appendChild(postElement);
                });
            } else {
                postsContainer.innerHTML = '<p>No posts found.</p>';
            }
        })
        .catch((error) => {
            console.error('Error fetching search results:', error);
        });
}

