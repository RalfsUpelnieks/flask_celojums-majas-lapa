document.addEventListener("DOMContentLoaded", () => {
    
    const SELECTORS = document.querySelectorAll(".selector");
    SELECTORS.forEach(selector => {
        selector.addEventListener("click", () => {
            if(selector.id != "selected") {
                pastSelected = document.getElementById("selected");

                pastSelected.id = "";
                selector.id = "selected";
            }
        });
    });
});