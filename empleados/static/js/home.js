document.addEventListener("DOMContentLoaded", () => {
  let alertElement = document.querySelector(".alert");

  // Si existe, eliminarla después de 5 segundos
  if (alertElement) {
    setTimeout(function () {
      alertElement.remove();
    }, 8000); // 8000 milisegundos = 8 segundos
  }
});
