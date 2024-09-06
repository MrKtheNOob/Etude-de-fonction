

const showhelpbtn = document.getElementById("showhelp")
const helpParagraph = document.getElementById("help-container")
var isShown = false

// Add event listener to each button

document.addEventListener("htmx:afterSwap", (event) => {
    if (event.target.id === "input-form") {
        MathJax.typesetPromise();  // Re-render MathJax
    }
});

document.getElementById("finput").addEventListener("input", function() {
    const mathContent = this.value; // Get the input value

    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML = mathContent // Set the value inside the div with LaTeX delimiters

    MathJax.typesetPromise([outputDiv]); // Render the MathJax in the div
});
// document.addEventListener("click",function(){
//     alert("body clicked")
//     if (isShown){
//         showhelpbtn.click()
//     }
// })

// Add the global click listener once, outside the showhelpbtn click handler
document.addEventListener("click", function(event) {
    if (isShown && !helpParagraph.contains(event.target) && !showhelpbtn.contains(event.target)) {
        // Click outside help paragraph and showhelpbtn
        showhelpbtn.click();
    }
});

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
