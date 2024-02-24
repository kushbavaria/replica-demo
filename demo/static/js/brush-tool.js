
function load() {
    let canvas = document.getElementById('bt-canvas');
    canvas.style.background = background.style.background;
    let mask = document.getElementById('mask-canvas');
    let paintButton = document.getElementById('paintbutton');
    let eraseButton = document.getElementById('erasebutton');
    let ctx = canvas.getContext('2d');
    let maskCtx = mask.getContext('2d');

    canvas.width = 611;
    canvas.height = 611;
    mask.width = canvas.width;
    mask.height = canvas.height;

    maskCtx.fillStyle = "#000";
    maskCtx.fillRect(0, 0, mask.width, mask.height)
    const alphaSlider = document.getElementById('alphaslider');
    const sizeSlider = document.getElementById('sizeslider');
    const colorPicker = document.getElementById('colorpicker');

    let drawColor = colorPicker.value;
    let drawAlpha = alphaSlider.value/alphaSlider.max;
    let drawWidth = sizeSlider.value;
    let painting = false;
    let paintButtonActive = false;
    let eraseButtonActive = false;

    let restoreArray = [];
    let maskArray = [];
    let redoArray = [];
    let maskRedoArray = [];
    let index = -1;

    function startPosition(e) {
        if (eraseButtonActive) {
            ctx.globalCompositeOperation = 'destination-out'; // Set composite operation to erase
            ctx.strokeStyle = 'rgba(0,0,0,0)'; // Set drawing color to transparent
            maskCtx.globalCompositeOperation = 'destination-out'; // Set composite operation to erase
            maskCtx.strokeStyle = 'rgba(0,0,0,0)'; // Set drawing color to transparent
            painting = true;
            draw(e);
        } else if (paintButtonActive) {
            maskCtx.globalCompositeOperation = 'source-over';
            ctx.globalCompositeOperation = 'source-over'; // Set composite operation to default (drawing)
            ctx.strokeStyle = colorPicker.value;
            maskCtx.strokeStyle = '#FFF'
            ctx.globalAlpha = alphaSlider.value;
            painting = true;
            draw(e);
        }
    }

    function finishedPosition(e) {
        maskCtx.beginPath();
        ctx.beginPath();
        if (painting && (paintButtonActive || eraseButtonActive)) {
            maskRedoArray = [];
            redoArray = [];
            let data = ctx.getImageData(0, 0, canvas.width, canvas.height);
            let maskData = maskCtx.getImageData(0, 0, mask.width, mask.height)
            restoreArray.push(data);
            maskArray.push(maskData);
            index++;
        }
        painting = false;
    }

    function draw(e) {
        if(!painting) return;
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        ctx.lineWidth = drawWidth;
        ctx.lineJoin = 'round';
        ctx.lineCap = 'round';
        ctx.strokeStyle = drawColor;
        ctx.globalAlpha = drawAlpha;

        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);


        maskCtx.lineWidth = drawWidth;
        maskCtx.lineJoin = 'round';
        maskCtx.lineCap = 'round';
        maskCtx.strokeStyle = '#FFF';

        maskCtx.lineTo(x, y);
        maskCtx.stroke();
        maskCtx.beginPath();
        maskCtx.moveTo(x, y);

    }

    canvas.addEventListener('mousedown', startPosition);
    canvas.addEventListener('mouseup', finishedPosition);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseout', finishedPosition);

    colorPicker.addEventListener('change', function() {
        drawColor = this.value; // Update drawColor to the selected color
    });

    alphaSlider.addEventListener('change', function() {
        drawAlpha = alphaSlider.value/alphaSlider.max;
        console.log(drawAlpha);
    })

    sizeSlider.addEventListener('change', function() {
        drawWidth = sizeSlider.value;
    })

    function clearCanvas() {
        maskCtx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        restoreArray = [];
        redoArray = [];
        maskArray = [];
        maskRedoArray = [];
        index = -1;
    }

    document.getElementById('bt-discard').addEventListener('click', clearCanvas);

    function togglePaint() {
        if (paintButtonActive) {
            this.classList.remove('tool-active');
            paintButtonActive = false;
        } else {
            this.classList.add('tool-active');
            paintButtonActive = true;
            eraseButton.classList.remove('tool-active');
            eraseButtonActive = false;
        }
    }
    paintButton.addEventListener('click', togglePaint)

    function toggleErase() {
        if (eraseButtonActive) {
            this.classList.remove('tool-active');
            eraseButtonActive = false;
        } else {
            this.classList.add('tool-active');
            eraseButtonActive = true;
            paintButton.classList.remove('tool-active');
            paintButtonActive = false;
        }
    }

    eraseButton.addEventListener('click', toggleErase)

    function undo() {
        if (index <= 0) {
            redoArray.push(restoreArray.pop()); // Save the current state for redo
            maskRedoArray.push(maskArray.pop());
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            maskCtx.fillRect(0, 0, canvas.width, canvas.height);
            restoreArray = [];
            maskArray = [];
            index = -1;
        } else {
            index -= 1;
            redoArray.push(restoreArray.pop());
            maskRedoArray.push(maskArray.pop());
            ctx.putImageData(restoreArray[index], 0, 0);
            maskCtx.putImageData(maskArray[index], 0, 0);
        }
    }

    function redo() {
        if (redoArray.length > 0) {
            let redoItem = redoArray.pop(); // Get the item from redoArray
            let redoMaskItem = maskRedoArray.pop();
            restoreArray.push(redoItem); // Put the item back to restoreArray
            maskArray.push(redoMaskItem);
            index = restoreArray.length - 1; // Update index
            ctx.putImageData(redoItem, 0, 0); // Redraw the item
            maskCtx.putImageData(redoMaskItem, 0, 0);
        }
    }

    const undoButton = document.getElementById('undo');
    undoButton.addEventListener('click', function() {
        if (restoreArray.length > 0) {
            undo();
        }
    });

    const redoButton = document.getElementById('redo');
    redoButton.addEventListener('click', redo);

    const modal = document.getElementById('modal')
    modal.addEventListener('click', closeBrushTool);

    let restoreBtn = document.getElementById('bt-restore');

    function restore() {
        clearCanvas()
        canvas.style.background = background.style.background;
    }
    restoreBtn.addEventListener('click', restore);

    let saveBtn = document.getElementById('bt-save');
    saveBtn.addEventListener('click', save);

    function save() {
        background.style.background = canvas.style.background;
        let pap = document.getElementById('pap');
        let img = document.getElementById(`imagen${currentImageIndex+1}`);
        img.src = pap.src;
        closeBrushTool();
    }


    function closeBrushTool() {
        modal.style.display = 'none';
        brushTool.style.display = 'none';
        paintButton.classList.remove('tool-active');
        eraseButton.classList.remove('tool-active');
        restore();
        clearCanvas();
        document.getElementById("bt-form").reset();
        document.getElementById('bt-container').remove();
    }

    const generateInpaint = document.getElementById("generate-inpaint");
    generateInpaint.addEventListener('click', generate);

    const loading = document.getElementById("bt-loading");

    function generate() {
        document.removeEventListener('click', generate);
        clearCanvas();
        eraseButtonActive = false;
        paintButtonActive = false;
        paintButton.classList.remove('tool-active');
        eraseButton.classList.remove('tool-active');
        paintButton.removeEventListener('click', togglePaint);
        eraseButton.removeEventListener('click', toggleErase);
        restoreBtn.removeEventListener('click', restore);
        saveBtn.removeEventListener('click', save);
        canvas.style.background = "#09090d";
        loading.style.display= 'flex';
    }

    let papcontainer = document.getElementById("papcontainer")

    papcontainer.addEventListener('htmx:afterSwap', function() {
        let canvas = document.getElementById('bt-canvas');
        let inpaint = document.getElementById("pap").src;
        canvas.style.background = `url(${inpaint})`;
        canvas.style.backgroundSize = 'contain';
        clearCanvas();
        paintButton.addEventListener('click', togglePaint);
        eraseButton.addEventListener('click', toggleErase);
        generateInpaint.addEventListener('click', generate);
        restoreBtn.addEventListener('click', restore);
        saveBtn.addEventListener('click', save);
        loading.style.display= 'none';
        const buttons = document.getElementsByClassName('big-btn');
        Array.from(buttons).forEach(button => {
            button.classList.remove('htmx-request');
        });
    })

}

function getCanvasImage() {
    const canvas = document.getElementById('bt-canvas')
    const computedStyle = window.getComputedStyle(canvas);
    const backgroundImage = computedStyle.backgroundImage;
    let imageURL = backgroundImage.slice(4, -1).replace(/"/g, "");
    toDataURL("image/jpeg");
    return canvasData.replace(/^data:image\/jpeg;base64,/, "");
}
function getMaskData() {
    // Convert canvas content to a base64-encoded JPEG
    const maskData = document.getElementById('mask-canvas').toDataURL("image/jpeg");

    // Remove the data URI prefix to get the raw base64 data
    return maskData.replace(/^data:image\/jpeg;base64,/, "");
}

load();
