function regenerateAvatar() {
    seed = window.crypto.randomUUID();
    avatar = "https://hostedboringavatars.vercel.app/api/beam?name=" + seed;
    document.getElementById('avatar-img').src = avatar;
}