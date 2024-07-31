let drawerHTML = '<div class="fixed top-0 w-screen h-screen bg-black bg-opacity-15" id="drawer" style="z-index: 50;"> <div class="flex flex-col p-12 text-sm bg-white h-screen" style="width: 400px;"> <div class="flex flex-row"> <h1 class="font-semibold text-2xl">Openbook</h1> <a href="/profile" class="ml-auto"><img class="w-10" id="avatar-img" src="{{avatar}}"></a> </div> <div class="flex flex-row space-x-8 my-12"> <button class="font-medium bg-black py-2 px-5 text-white rounded-full">Pages</button> <button class="font-medium py-2 px-5 rounded-full hover:bg-black hover:bg-opacity-10">Books</button> </div> <div class="flex flex-col space-y-2"> <a href="/recent-textbook" class="hover:font-semibold">Recent textbook</a> <a href="/library" class="font-semibold">Library</a> <a href="/upload-centre" class="hover:font-semibold">Uploads centre</a> </div> <a href="/log-out" class="mt-auto bottom-0 hover:font-semibold">Log out</a> </div> </div>';

function closeDrawer() {
    document.getElementById("drawer-wrapper").innerHTML = '';
}

function openDrawer() {
    document.getElementById("drawer-wrapper").innerHTML = drawerHTML;
}