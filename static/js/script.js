const showhelpbtn = document.getElementById("showhelp")
const helpParagraph = document.getElementById("help-container")
var isShown = false


document.addEventListener("htmx:afterSwap", (event) => {
    if (event.target.id === "input-form") {
        MathJax.typesetPromise();  // Re-render MathJax
    }
});

// Add the global click listener once, outside the showhelpbtn click handler
document.addEventListener("click", function(event) {
    if (isShown && !helpParagraph.contains(event.target) && !showhelpbtn.contains(event.target)) {
        // Click outside help paragraph and showhelpbtn
        showhelpbtn.click();
    }
});


//logic for the help button
showhelpbtn.addEventListener("click", function (event) {
    // Prevent this event from bubbling up and triggering the global click listener
    event.stopPropagation();
    isShown = !isShown;
    if (isShown) {
        helpParagraph.classList.add("clicked");
        document.querySelectorAll("body,button,input").forEach(element => {
            element.style.backgroundColor = "#988d7f";
        });
        document.getElementById("showhelp").style.backgroundColor = "#f0f0f0";
        helpParagraph.style.visibility = "visible";
    } else {
        helpParagraph.classList.remove("clicked");
        document.body.style.backgroundColor = "#faebd7";
        document.querySelectorAll("input").forEach(element => {
            element.style.backgroundColor = "#ffffff";
        });
        helpParagraph.style.visibility = "hidden";
        document.querySelectorAll("button").forEach(button => {
            button.style.backgroundColor = "#f0f0f0";
        });
    }
});
