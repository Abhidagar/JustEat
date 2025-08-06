document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".cuisine-card");
  const select = document.querySelector("[data-role='select-cuisine']");

  cards.forEach((card) => {
    const value = card.dataset.value;
    const option = [...select.options].find((opt) => opt.value === value);

    // Initial selection
    if (card.dataset.selected === "True") {
      card.classList.add("selected", "text-bg-success");
      option.selected = true;
    }

    card.style.cursor = "pointer";

    card.addEventListener("click", () => {
      const isSelected = card.classList.toggle("selected");
      option.selected = isSelected;
      card.classList.toggle("text-bg-success", isSelected);
    });
  });
});
