function toggleLike(postId) {
    fetch('/post/' + postId + '/like', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const likeCount = document.getElementById('like-count-' + postId);
        likeCount.textContent = data.likes_count + ' likes';

        // Conditional styling for likes
        if (data.likes_count > 0) {
            likeCount.classList.add('like-count-active');
        } else {
            likeCount.classList.remove('like-count-active');
        }

        // Update button text based on like/unlike status
        const likeButton = likeCount.nextElementSibling;
        likeButton.textContent = data.liked ? 'Unlike' : 'Like';
        // Remove focus from the button
        likeButton.blur();
    });
}

function showNewPostForm() {
    document.getElementById('new-post-form').style.display = 'block';
    document.getElementById('new-post-btn').style.display = 'none';
}

function hideNewPostForm() {
    document.getElementById('new-post-form').style.display = 'none';
    document.getElementById('new-post-btn').style.display = 'block';
}

function submitNewPost() {
    const content = document.getElementById('new-post-content').value;

    if (!content.trim()) {
        alert("Please write something for your post.");
        return;
    }

    fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        }),
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.message) {
            hideNewPostForm();
            document.getElementById('new-post-content').value = ''; // Clear the textarea
            location.reload(); // Reload the page to show the new post
        } else {
            alert(result.error);
        }
    });
}

function editPost(postId) {
        document.getElementById('post-content-' + postId).style.display = 'none';
        document.getElementById('post-edit-' + postId).style.display = 'block';
    }

    function savePost(postId) {
        const content = document.getElementById('edit-content-' + postId).value;
        fetch('/post/' + postId + '/edit', {
            method: 'POST',
            body: JSON.stringify({
                content: content
            }),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(result => {
            if(result.message) {
                // Update only the text content of the post
                const postContentP = document.querySelector('#post-content-' + postId + ' p.card-text');
                postContentP.textContent = content;

                // Display the updated content and ensure the Edit button is still visible
                document.getElementById('post-content-' + postId).style.display = 'block';
                document.getElementById('post-edit-' + postId).style.display = 'none';
                } else {
                    alert(result.error);
                }
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