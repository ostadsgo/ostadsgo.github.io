// toggle hamberguer menu
const ham = document.querySelector(".ham");
const leftMenu = document.querySelector(".menu ul");
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

/* Switch theme */
const switcher = document.querySelector(".switcher");
const switcherIcon = document.querySelector(".switcher i");
const body = document.body;
switcher.addEventListener("click", () => {
  if (body.classList.contains("light")) {
    body.classList.remove("light");
    body.classList.add("dark");
    switcherIcon.classList.add("fa-sun");
    switcherIcon.classList.remove("fa-moon");
    console.log("switch to dark theme.");
  } else {
    body.classList.remove("dark");
    body.classList.add("light");
    switcherIcon.classList.remove("fa-sun");
    switcherIcon.classList.add("fa-moon");
    console.log("switch to light theme.");
  }
});

/* Update progressbar */

// Script to handle scroll progress
window.onscroll = function () {
  updateProgressBar();
};

function updateProgressBar() {
  const scrollTop =
    document.documentElement.scrollTop || document.body.scrollTop;
  const scrollHeight =
    document.documentElement.scrollHeight -
    document.documentElement.clientHeight;
  const scrolled = (scrollTop / scrollHeight) * 100;
  const progressBar = document.getElementById("progressBar");
  if (progressBar != null) {
    document.getElementById("progressBar").style.width = scrolled + "%";
  }
}
