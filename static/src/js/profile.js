function regenerateAvatar() {
    seed = window.crypto.randomUUID();
    avatar = "https://hostedboringavatars.vercel.app/api/beam?name=" + seed;
    document.getElementById('avatar-img').src = avatar;
}

function saveChanges() {
    var data = {
        "avatar": document.getElementById('avatar-img').src,
        "display-name": document.getElementById('display-name').value,
        "year-level": document.getElementById('year-level').value,
    };

    Object.keys(data).forEach(key => {
        if (data[key] == null || data[key] == "") {
            delete data[key];
        }
    });

    fetch('/update-profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            location.href = location.origin + location.pathname + '?editing=0';
        }
    });
}