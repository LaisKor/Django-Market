document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.toggle-like-btn')
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            fetch(`/items/${itemId}/toggle_like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                this.textContent = data.liked ? '찜 해제' : '찜하기';
                this.classList.toggle('liked', data.liked);
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

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