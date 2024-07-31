function deleteSubmission(id) {
    fetch('/delete-submission', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'submission-id': id})
    }).then(response => {
        if (response.ok) {
            document.getElementById('s-' + id).remove();
        }
    });
}

function approveSubmission(repository, id) {
    fetch('/approve-submission', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'repository': repository, 'submission-id': id})
    }).then(response => {
        if (response.ok) {
            document.getElementById('s-' + id).remove();
        }
    });
}