  // script.js
  document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".toggle-button");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            const targetDiv = document.getElementById(targetId);

            // Esconder todas as divs
            document.querySelectorAll(".toggle-div").forEach(div => {
                div.style.display = "none";
            });

            // Mostrar a div correspondente ao botão clicado
            if (targetDiv) {
                targetDiv.style.display = "block";
            }
        });
    });
});