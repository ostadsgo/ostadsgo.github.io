// toggle hamberguer menu
const ham = document.querySelector(".ham");
const leftMenu = document.querySelector(".left-menu ul");
const hamIcon = document.querySelector(".ham i");

ham.addEventListener("click", () => {
  leftMenu.classList.toggle("active");
  if (leftMenu.classList.contains("active")) {
    hamIcon.classList.remove("rotate-out");
    hamIcon.classList.add("rotate-in"); // Animate to cross (X)
    setTimeout(() => {
      hamIcon.classList.remove("fa-bars");
      hamIcon.classList.add("fa-xmark");
      hamIcon.classList.remove("rotate-in"); // Animate to cross (X)
    }, 400);
  } else {
    hamIcon.classList.add("rotate-in"); // Animate to cross (X)
    setTimeout(() => {
      hamIcon.classList.remove("fa-xmark");
      hamIcon.classList.add("fa-bars");
      hamIcon.classList.remove("rotate-in"); // Animate to cross (X)
      hamIcon.classList.add("rotate-out"); // Animate to cross (X)
    }, 400);
  }
});

// Close the menu when clicking outside the menu or hamburger
document.addEventListener("click", (event) => {
  // Check if the clicked target is not the menu or hamburger
  if (!leftMenu.contains(event.target) && !ham.contains(event.target)) {
    leftMenu.classList.remove("active"); // Close the menu
    // remove x icon if after user clicked anywhere of page.
    if (hamIcon.classList.contains("fa-xmark")) {
      hamIcon.classList.remove("fa-xmark");
      hamIcon.classList.add("fa-bars");
    }
  }
});

