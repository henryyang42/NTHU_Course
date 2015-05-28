$("#saveAsFile").click(function() {
  html2canvas($("#course-table")).then(function(canvas) {
    var bgcanvas = document.createElement("canvas");
    bgcanvas.width = canvas.width;
    bgcanvas.height = canvas.height;
    var ctx = bgcanvas.getContext("2d");
    var gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, "rgba(255, 255, 255, 0.9)");
    gradient.addColorStop(1, "rgba(221, 232, 255, 0.9)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(canvas, 0, 0, canvas.width, canvas.height);

    var data = bgcanvas.toDataURL("image/png");
    data = data.replace("image/png", "image/octet-stream");
    var downloadLink = document.createElement("a");
    downloadLink.href = data;
    downloadLink.download = "course-table.png";

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  });
});
