document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".scroll-content").forEach((wrapper) => {
    const updateShadows = () => {
      const scrollLeft = wrapper.scrollLeft;
      const maxScrollLeft = wrapper.scrollWidth - wrapper.clientWidth;

      console.log(scrollLeft > 5, scrollLeft < maxScrollLeft - 5);

      wrapper.parentElement.classList.toggle("scroll-left", scrollLeft > 5);
      wrapper.parentElement.classList.toggle("scroll-right", scrollLeft < maxScrollLeft - 5);
    };

    wrapper.addEventListener("scroll", updateShadows);
    window.addEventListener("resize", updateShadows);
    updateShadows(); // initial call
  });
});
