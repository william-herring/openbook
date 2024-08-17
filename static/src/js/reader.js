function showDownloadPrompt() {
    document.getElementById('download-prompt').style.display = 'flex';
}

function closeDownloadPrompt() {
    document.getElementById('download-prompt').style.display = 'none';
}

function showChaptersList() {
    document.getElementById('questions-toggle').className = 'font-medium py-2 px-5 rounded-full hover:bg-black hover:bg-opacity-10';
    document.getElementById('chapters-toggle').className = 'font-medium bg-black py-2 px-5 text-white rounded-full';
    document.getElementById('questions-list').className = 'hidden';
    document.getElementById('chapters-list').className = 'flex flex-col space-y-4 h-full overflow-y-scroll';
}

function showQuestionsList() {
    document.getElementById('chapters-toggle').className = 'font-medium py-2 px-5 rounded-full hover:bg-black hover:bg-opacity-10';
    document.getElementById('questions-toggle').className = 'font-medium bg-black py-2 px-5 text-white rounded-full';
    document.getElementById('chapters-list').className = 'hidden';
    document.getElementById('questions-list').className = 'flex flex-col space-y-4 h-full overflow-y-scroll';
}