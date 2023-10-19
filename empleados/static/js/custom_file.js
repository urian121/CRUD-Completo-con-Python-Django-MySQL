// Obtén todos los elementos con la clase "fileInput"
var fileInputs = document.querySelectorAll(".fileInput");

// Itera a través de cada elemento con la clase "fileInput"
fileInputs.forEach(function (fileInput) {
  // Agrega un event listener para el evento "change" a cada elemento
  fileInput.addEventListener("change", function () {
    var numfiles = this.files.length;
    var parent = this.closest(".input-file");

    // Elimina los elementos "ins" existentes
    var existingInsElements = parent.querySelectorAll("ins");
    existingInsElements.forEach(function (insElement) {
      parent.removeChild(insElement);
    });

    // Agrega los nuevos elementos "ins" con los nombres de los archivos
    for (var i = 0; i < numfiles; i++) {
      var insElement = document.createElement("ins");
      insElement.textContent = this.files[i].name;
      parent.appendChild(insElement);
    }
  });
});
