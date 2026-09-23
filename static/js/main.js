(function () {
  const themes = [
    { value: "light", label: "White / soft gray" },
    { value: "cream", label: "Warm cream" },
    { value: "contrast", label: "Black / white" },
    { value: "navy", label: "Deep navy" },
  ];
  const picker = document.createElement("div");
  picker.className = "theme-picker";
  picker.innerHTML = '<label for="theme-select">Preview</label><select id="theme-select" aria-label="Choose background theme"></select>';
  const select = picker.querySelector("select");
  themes.forEach((theme) => {
    const option = document.createElement("option");
    option.value = theme.value;
    option.textContent = theme.label;
    select.appendChild(option);
  });

  const savedTheme = localStorage.getItem("portfolio-theme") || "cream";
  document.body.dataset.theme = savedTheme;
  select.value = savedTheme;
  document.body.appendChild(picker);
  select.addEventListener("change", () => {
    document.body.dataset.theme = select.value;
    localStorage.setItem("portfolio-theme", select.value);
  });

  const menuBtn = document.getElementById("menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  const iconOpen = document.getElementById("icon-open");
  const iconClose = document.getElementById("icon-close");

  if (!menuBtn || !mobileMenu) return;

  menuBtn.addEventListener("click", () => {
    const isOpen = mobileMenu.style.maxHeight && mobileMenu.style.maxHeight !== "0px";

    if (isOpen) {
      mobileMenu.style.maxHeight = "0px";
      mobileMenu.style.opacity = "0";
      menuBtn.setAttribute("aria-expanded", "false");
    } else {
      mobileMenu.style.maxHeight = mobileMenu.scrollHeight + "px";
      mobileMenu.style.opacity = "1";
      menuBtn.setAttribute("aria-expanded", "true");
    }

    iconOpen.classList.toggle("hidden");
    iconClose.classList.toggle("hidden");
  });

  // Close the menu automatically if the viewport grows past the mobile breakpoint
  window.addEventListener("resize", () => {
    if (window.innerWidth >= 768) {
      mobileMenu.style.maxHeight = "0px";
      mobileMenu.style.opacity = "0";
      menuBtn.setAttribute("aria-expanded", "false");
      iconOpen.classList.remove("hidden");
      iconClose.classList.add("hidden");
    }
  });
})();
