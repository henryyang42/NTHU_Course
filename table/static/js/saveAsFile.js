$("#saveAsFile").click(function() {
  console.log("Click " + $("#course-table").css("border-color"));
  $("#course-table").css("border", "1px solid black")
  $("#course-table > tr").css("border", "1px solid black");
  $("#course-table > th").css("border", "1px solid black");
  $("#course-table > td").css("border", "1px solid black");
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
    console.log(canvas.width + " " + canvas.height);
    //document.body.appendChild(canvas);
    console.log(bgcanvas.width + " " + bgcanvas.height);
    //document.body.appendChild(bgcanvas);
    ctx.drawImage(canvas, 0, 0, canvas.width, canvas.height);
    console.log(bgcanvas.width + " " + bgcanvas.height);
    document.body.appendChild(bgcanvas);

    var data = bgcanvas.toDataURL("image/png");
    data = data.replace("image/png", "image/octet-stream");
    var downloadLink = document.createElement("a");
    downloadLink.href = data;
    downloadLink.download = "course-table.png";

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  });
  $("#course-table").css("border-color", "");
  $("#course-table > tr").css("border-color", "");
  $("#course-table > th").css("border-color", "");
  $("#course-table > td").css("border-color", "");
});
