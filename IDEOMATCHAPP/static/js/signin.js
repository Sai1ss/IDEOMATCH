document.addEventListener("DOMContentLoaded", () => {
  // Regex para RUT SIN puntos, con guión y dígito verificador
  const rutRegex = /^\d{7,8}-[\dkK]$/i;

  // Selecciona los inputs
  const rutInput  = document.getElementById("id_username");
  const passInput = document.getElementById("id_password");
  const inputs    = document.querySelectorAll(".form-group input");

  // Enfocar/Desenfocar para animaciones de borde
  inputs.forEach(input => {
    input.addEventListener("focus", () => {
      input.style.borderColor = "#1e3c72";
      input.parentElement.classList.add("focused");
    });
    input.addEventListener("blur", () => {
      input.style.borderColor = "#ccc";
      input.parentElement.classList.remove("focused");
    });
  });

  // Validar RUT en cada pulsación
  if (rutInput) {
    rutInput.addEventListener("input", () => {
      const val = rutInput.value.trim();
      // limpia clases anteriores
      rutInput.classList.remove("is-valid", "is-invalid");
      if (rutRegex.test(val)) {
        rutInput.classList.add("is-valid");
      } else {
        rutInput.classList.add("is-invalid");
      }
    });
  }

  // Validar contraseña no vacía
  if (passInput) {
    passInput.addEventListener("input", () => {
      passInput.classList.remove("is-valid", "is-invalid");
      if (passInput.value.trim().length > 0) {
        passInput.classList.add("is-valid");
      }
    });
  }

  // Card hover animation (opcional)
  const card = document.querySelector(".signin-card");
  if (card) {
    card.addEventListener("mouseover", () => card.style.transform = "scale(1.02)");
    card.addEventListener("mouseout",  () => card.style.transform = "scale(1)");
  }
});
