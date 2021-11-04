document.addEventListener("DOMContentLoaded", () => {

    const LOGIN_BUTTON = document.getElementById("login");
    const LOGIN_POPUP = document.getElementById("log-in-panel");

    isLoggedIn = false;

    LOGIN_BUTTON.addEventListener("click", () => {
        if(isLoggedIn === false){
            let login = prompt("Ievadiet jūsu lietotājvārdu!");
            let pass = prompt("Ievadiet jūsu paroli!");
            if (login === "user" && pass === "user") {
                alert("Ielogošanās veiksmīga!");
                isLoggedIn = true;
            }
            else {
                alert("Lietotājvārds vai parole ir nepareiza.")
            }
        }
        else {
            window.location.href = "/profils";
        }
    });
});