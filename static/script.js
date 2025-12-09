function previewImage(event) {
    const input = event.target;
    const previewContainer = document.getElementById("preview-container");
    const previewImg = document.getElementById("preview-img");
    const previewFilename = document.getElementById("preview-filename");

    if (input.files && input.files[0]) {
        const file = input.files[0];
        previewImg.src = URL.createObjectURL(file);
        previewFilename.textContent = file.name;
        previewContainer.style.display = "grid";
    } else {
        previewContainer.style.display = "none";
    }
}

// Set probability bar widths from data-width attribute
document.addEventListener("DOMContentLoaded", () => {
    const bars = document.querySelectorAll(".prob-bar");
    bars.forEach(bar => {
        const width = bar.getAttribute("data-width");
        if (width !== null) {
            bar.style.width = width + "%";
        }
    });
});
