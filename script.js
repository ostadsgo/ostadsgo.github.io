


// how many page I've been red form 
let pages = document.getElementById("value").textContent;
let red_page = parseInt(pages.split(" ")[1]);
let total_pages = parseInt(pages.split(" ")[3]);

// Calculate done percteged 
let done_percentage = Math.round((100 / total_pages) * red_page);
let done_percentage_format = `${done_percentage}%`;
let progress = document.getElementById("progress");
progress.innerHTML = done_percentage_format;
// Update width of the progress in progressbar
progress.style.width = done_percentage_format;