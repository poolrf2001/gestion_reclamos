$(document).ready(function(){
    function hideDetailsButton() {
        $("#verDetallesBtn").hide();
    }

    function redirectToHome() {
        window.location.href = "/reclamos/consulta/";
    }

    $("#reclamoModal").on('hidden.bs.modal', function () {
        hideDetailsButton();
        redirectToHome();
    });

    $("#closeModal").click(function(){
        hideDetailsButton();
        redirectToHome();
    });

    function disableBack() {
        window.history.forward();
    }

    window.onload = disableBack();
    window.onpageshow = function(evt) {
        if (evt.persisted) disableBack();
    }

    // Mostrar el popup cuando hay reclamos
    if ($("#alertaReclamo").length) {
        $("#alertaReclamo").modal('show');
    } else if ($("#alertaNoReclamo").length) {
        $("#alertaNoReclamo").modal('show');
    }
});

function validateForm() {
    var codigo = document.getElementById('codigo').value;
    if (!codigo) {
        alert("Por favor, ingrese el código del reclamo.");
        return false;
    }
    return true;
}
