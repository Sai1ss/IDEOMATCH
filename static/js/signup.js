document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const inputs = form.querySelectorAll("input, select");
  const submitBtn = form.querySelector("button[type='submit']");

  const validateField = (input) => {
    const errorBox = input.closest(".form-group").querySelector(".error-msg");
    let valid = true;

    // Simple reglas
    if (input.name.includes("email")) {
      valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value);
    } else if (input.name.includes("rut")) {
      valid = /^[0-9]{7,8}-[0-9kK]$/.test(input.value);
    } else if (input.name.includes("edad")) {
      valid = input.value && parseInt(input.value) >= 13;
    } else if (input.name.includes("password")) {
      valid = input.value.length >= 8;
    } else {
      valid = input.value.trim().length > 0;
    }

    // Aplica estilos visuales
    input.classList.remove("is-valid", "is-invalid");
    if (valid) {
      input.classList.add("is-valid");
      if (errorBox) errorBox.textContent = "";
    } else {
      input.classList.add("is-invalid");
      if (errorBox) errorBox.textContent = "Este campo no es válido.";
    }

    return valid;
  };

  inputs.forEach(input => {
    input.addEventListener("input", () => {
      validateField(input);
      validateForm();
    });
  });

  const validateForm = () => {
    let allValid = true;
    inputs.forEach(input => {
      if (!validateField(input)) {
        allValid = false;
      }
    });
    submitBtn.disabled = !allValid;
  };

  validateForm(); // Inicial
});
