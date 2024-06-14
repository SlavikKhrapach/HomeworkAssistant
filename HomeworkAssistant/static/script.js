document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded and ready.');

    window.fetchAssignments = function() {
        const form = document.getElementById('fetchAssignmentsForm');
        const formData = new FormData(form);

        fetch('/assignments', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html;
        })
        .catch(error => {
            console.error('Error fetching assignments:', error);
        });
    };
});