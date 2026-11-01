
let images = [
    "https://picsum.photos/id/1015/600/400",
    "https://picsum.photos/id/1016/600/400",
    "https://picsum.photos/id/1018/600/400",
    "https://picsum.photos/id/1020/600/400",
    "https://picsum.photos/id/1024/600/400",
    "https://picsum.photos/id/1035/600/400"
];

let currentIndex = 0;

// Display images in gallery
let gallery = document.getElementById("gallery");

images.forEach((image, index) => {
    let img = document.createElement("img");

    img.src = image;
    img.onclick = function () {
        openSlide(index);
    };

    gallery.appendChild(img);
});

// Open slideshow
function openSlide(index) {
    currentIndex = index;

    document.getElementById("slideshow").style.display = "block";

    showImage();
}

// Display current image
function showImage() {
    document.getElementById("slideImage").src =
        images[currentIndex];
}

// Next image
function nextImage() {
    currentIndex++;

    if (currentIndex >= images.length) {
        currentIndex = 0;
    }

    showImage();
}

// Previous image
function prevImage() {
    currentIndex--;

    if (currentIndex < 0) {
        currentIndex = images.length - 1;
    }

    showImage();
}

// Close slideshow
function closeSlide() {
    document.getElementById("slideshow").style.display = "none";
}

// Auto-play slideshow
setInterval(function () {
    if (document.getElementById("slideshow").style.display === "block") {
        nextImage();
    }
}, 3000);
