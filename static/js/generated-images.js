
function getImages() {
    return [document.getElementById("imagen1").src,
        document.getElementById("imagen2").src,
        document.getElementById("imagen3").src];
}

imgCounter.innerText = `${currentImageIndex+1}/3`
background.style.background = `url(${getImages()[0]})`;
background.style.backgroundSize = 'contain';
function cycleImages() {
    currentImageIndex = (currentImageIndex + 1) % 3;
    imgCounter.innerText = `${currentImageIndex+1}/3`
    background.style.background = `url(${getImages()[currentImageIndex]})`;
    background.style.backgroundSize = 'contain';
}

function cycleImagesLeft() {
    currentImageIndex = (currentImageIndex - 1 + 3) % 3;
    imgCounter.innerText = `${currentImageIndex+1}/3`
    background.style.background = `url(${getImages()[currentImageIndex]})`;
    background.style.backgroundSize = 'contain';
}
arrowLeft.addEventListener('click', cycleImagesLeft);
arrowRight.addEventListener("click", cycleImages);
