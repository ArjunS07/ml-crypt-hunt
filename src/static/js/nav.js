nav = document.getElementById("nav");
navToggle = document.getElementById("nav-toggle");
navItemsContainer = document.getElementById("nav-items-container");

navToggle.addEventListener("click", function() {
    if (navItemsContainer.classList.contains("hidden")) {
        // The nav is currently collapsed, so we want to expand it
        navItemsContainer.classList.remove("hidden");
        navItemsContainer.classList.add("block");

        // Make the color of the entire nav zinc-100 and dark:zinc-900
        nav.classList.add("bg-zinc-50");
        nav.classList.add("dark:bg-zinc-900");
    }
    else {
        // The nav is currently expanded, so we want to collapse it
        navItemsContainer.classList.remove("block");
        navItemsContainer.classList.add("hidden");

        // Remove the color of the entire nav
        nav.classList.remove("bg-zinc-50");
        nav.classList.remove("dark:bg-zinc-900");
    }
});