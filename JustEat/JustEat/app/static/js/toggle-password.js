document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll("[data-role='password-toggle']");

  buttons.forEach((button) =>
    button.addEventListener("click", togglePasswordVisibility)
  );
}); 

/**
 * Toggles the visibility of a password field when a button is clicked.
 *
 * This function finds the target input field (specified in the button's `data-target` attribute),
 * switches its type between "password" and "text", and updates the eye icon accordingly.
 *
 * @param {Event} event - The click event triggered by the button.
 */
function togglePasswordVisibility(event) {
  // Get the button that was clicked
  const btn = event.currentTarget;

  // Retrieve the target input field ID from the button's `data-target` attribute
  const targetId = btn.dataset.target;
  const targetElement = document.getElementById(targetId);

  // Target input field not found
  if (!targetElement) return;

  const isPassword = targetElement.type === "password";
  const icon = btn.querySelector("i");

  targetElement.type = isPassword ? "text" : "password"; // toggle input type

  if (!icon) return;

  // Change icon accordingly
  icon.classList.toggle("bi-eye", !isPassword);
  icon.classList.toggle("bi-eye-slash", isPassword);
}
