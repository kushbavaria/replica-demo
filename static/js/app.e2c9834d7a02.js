let modal = document.getElementById('modal');

let browseBtn = document.getElementById('browse');

let celebBrowser = document.getElementById('celeb-browser')

let currentImageIndex = 0; // Start with the first image

let canEdit = "false";

browseBtn.addEventListener('click', openCelebBrowser);

function openCelebBrowser() {
    modal.style.display = 'block';
    celebBrowser.style.display = 'flex';
}

modal.addEventListener('click', closeCelebBrowser);

function closeCelebBrowser() {
    modal.style.display = 'none';
    celebBrowser.style.display = 'none';
}

let celebCards = document.getElementsByClassName('cb-card');
let celebInput = document.getElementById('celebrity');

function celebSelect(celebCard) {
    celebInput.value = celebCard.getElementsByClassName('cb-name')[0].innerText;
    closeCelebBrowser();
}

function updateCards() {
    for (let i = 0; i < celebCards.length; i++) {
        celebCards[i].addEventListener('click', function () {
            celebSelect(celebCards[i]);
        });
    }
}
let background = document.getElementById("main-img");
let arrowLeft = document.getElementById('arrow-left');
let arrowRight = document.getElementById('arrow-right');

document.getElementById('generate-btn').addEventListener('click', loadingText)

let brushBtn = document.getElementById('brush-btn');
background.addEventListener('htmx:afterSwap', function() {
    document.getElementById('generate-btn').classList.remove('htmx-request');
    brushBtn.classList.remove('htmx-request');
    checkContent();
    document.getElementById('download-btn').addEventListener('click', downloadImage);
    canEdit = true;
})

let generatedImages = document.getElementById('generated-images')

function loadingText() {
    generatedImages.innerHTML = "<span id=\"loading-robot\" class=\"material-symbols-outlined loading-robot\" " +
        "style=\"margin-bottom: 20px; transform: scale(1.9)\">smart_toy</span>\n" +
        "Generating your images...";
    document.getElementById("main-img").style.background = '#14161f';
    document.getElementById('download-btn').removeEventListener('click', downloadImage);
    imgCounter.innerText = `${1}/1`
    canEdit = false;
}


let imgCounter = document.getElementById("img-counter");


let prompt = document.getElementById('prompt');

prompt.addEventListener('input', checkContent);
celebInput.addEventListener('input', checkContent);

function checkContent() {
    if (prompt.value.trim() !== '' && celebInput.value.trim() !== '') {
        document.getElementById('generate-btn').classList.remove('htmx-request');
    } else {
        document.getElementById('generate-btn').classList.add('htmx-request');
   }
}

checkContent();

function generateRandomFileName() {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let randomString = '';
  for (let i = 0; i < 10; i++) {
    randomString += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return randomString;
}

// Function to get the background image URL of a div
function getBackgroundImageUrl(element) {
    // Get the computed style of the div
    const computedStyle = window.getComputedStyle(element);
    // Extract the background image URL from the computed style
    const backgroundImage = computedStyle.backgroundImage;
    // Remove 'url(' and ')' from the URL
    return backgroundImage.slice(4, -1).replace(/"/g, "");
}

function downloadImage() {
    // Get the background image URL of the div
    const backgroundImageUrl = getBackgroundImageUrl(document.getElementById('main-img'));
    // Generate a random filename
    const fileName = generateRandomFileName();
    // Create a temporary anchor element to trigger the download
    const link = document.createElement('a');
    link.href = backgroundImageUrl;
    link.download = fileName;

    // Append the anchor element to the document body
    document.body.appendChild(link);

    // Programmatically click the anchor element to initiate the download
    link.click();

    // Remove the anchor element from the document body after a short delay
    setTimeout(function() {
      document.body.removeChild(link);
    }, 100);
}

let brushTool = document.getElementById('brush-tool');


brushBtn.addEventListener('click', openBrushTool);



function openBrushTool() {
    if (canEdit) {
        modal.style.display = 'block';
        brushTool.style.display = 'flex';
    } else {
        let brushTool = document.getElementById('bt-container');
        brushTool.remove();
    }
}




