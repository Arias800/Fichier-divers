// ==UserScript==
// @name         Equipe login block
// @version      0.0.1
// @description  Skip Equipe Login
// @author       Arias800
// @match        *://live.lequipe.fr/*
// ==/UserScript==
function SomeFunction(e) {
    if (window.location.href.indexOf("video") > -1)
    {
        console.log("Redirect to daylimotion");
        window.location = "https://www.dailymotion.com/embed/video/" + window.location.href.split("/").pop();
        document.body.removeEventListener("DOMNodeInserted", SomeFunction, true);
        console.log("Res appeared.");
    }
}

if(document.getElementById('res')) {
    console.log('Res already existed');
} else {
    document.body.addEventListener("DOMNodeInserted", SomeFunction, true);
}
