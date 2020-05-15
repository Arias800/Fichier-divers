// ==UserScript==
// @name         ReCaptcha
// @match        *://ed-protect.org/*
// @match        *://www.google.com/recaptcha/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

// ==Code==
const url = window.location !== window.parent.location ? document.referrer : document.location.href;
if (location.href.includes("google.com/recaptcha")) {
    var clickCheck = setInterval(function() {
        if (document.querySelectorAll(".recaptcha-checkbox-checkmark").length > 0) {
            clearInterval(clickCheck);
            document.querySelector(".recaptcha-checkbox-checkmark").click();
        }
    }, 50);
} else {
    window.onload = readyToHelp;
}

function readyToHelp() {
    var execCheck = setInterval(function() {
        if (window.grecaptcha && window.grecaptcha.execute) {
            clearInterval(execCheck);
            try { window.grecaptcha.execute(); } catch(e) {}
        }
    }, 50);
    [...document.forms].forEach(form => {
        if (form.innerHTML.includes("google.com/recaptcha")) {
            var solveCheck = setInterval(function() {
                if (window.grecaptcha && !!grecaptcha.getResponse()) {
                    clearInterval(solveCheck);
                    form.submit();
                }
            }, 50);
        }
    });
}

// ==/Code==

(function() {
    var origOpen = XMLHttpRequest.prototype.open;
    console.log(origOpen);
    XMLHttpRequest.prototype.open = function() {
        console.log('request started!');
        this.addEventListener('load', function() {
            console.log('request completed!');
            if (this.responseText.includes('uvresp'))
            {
                var re = new RegExp(/"uvresp","(.+?)"/);
                var match = re.exec(this.responseText);
                console.log("Recaptcha Token : " + match[1]);
            }
        });
        origOpen.apply(this, arguments);
    };
})();

