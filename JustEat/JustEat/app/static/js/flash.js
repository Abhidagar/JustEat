document.addEventListener("DOMContentLoaded", function () {
  const bsAlerts = document.querySelectorAll(".alert");

  bsAlerts.forEach((alert) =>
    alert.addEventListener("click", handleAlertClose)
  );

  // Auto-hide flash messages after 2 seconds
  setTimeout(() => {
    document.querySelectorAll(".alert .btn-close").forEach((el) => {
      if (el) {
        el.click();
      }
    });
  }, 2000);
});

function handleAlertClose(event) {
  const parent = event.currentTarget.parentElement;

  if (!parent) return;

  parent.classList.add("animate-pop-out");
  parent.classList.remove("animate-pop-in");

  setTimeout(() => {
    parent.remove();
  }, 300);
}
