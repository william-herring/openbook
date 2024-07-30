function regenerateAvatar() {
    seed = window.crypto.randomUUID();
    avatar = "https://hostedboringavatars.vercel.app/api/beam?name=" + seed;
    document.getElementById('avatar-img').src = avatar;
}

function saveChanges() {
    console.log(document.getElementById('display-name').value);
    console.log(document.getElementById('year-level') == null);

    fetch('/update-profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "avatar": document.getElementById('avatar-img').src,
            "display-name": document.getElementById('display-name').value,
            "year-level": document.getElementById('year-level').value,
        })
    }).then(response => {
        if (response.ok) {
            const url = new URL(window.location.href);
            const params = new URLSearchParams(url.search);
            params.delete('editing');
        }
    });
    console.log('hi');
}