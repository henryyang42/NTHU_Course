$("#postToFB").click(function() {
  var pre_message = "My tentative course selection";
  var nthu_course_link = "by http://nthu-course.cf";
  var img_message = pre_message + "\n" + nthu_course_link;
  html2canvas($("#course-table")).then(function(canvas) {
    var data = canvas.toDataURL("image/png");
    var encodedPng = data.substring(data.indexOf(',') + 1, data.length);
    var decodedPng = Base64Binary.decode(encodedPng);
    FB.getLoginStatus(function(response) {
      if (response.status === "connected") {
        postImageToFacebook(response.authResponse.accessToken, "NTHU Course", "image/png", decodedPng, img_message);
      } else if (response.status === "not_authorized") {
        FB.login(function(response) {
          postImageToFacebook(response.authResponse.accessToken, "NTHU Course", "image/png", decodedPng, img_message);
        }, {
          scope: "publish_actions"
        });
      } else {
        FB.login(function(response) {
          postImageToFacebook(response.authResponse.accessToken, "NTHU Course", "image/png", decodedPng, img_message);
        }, {
          scope: "publish_actions"
        });
      }
    });
  });

  // Redefine sendAsBinary method
  XMLHttpRequest.prototype.sendAsBinary = function(sData) {
    var nBytes = sData.length,
      ui8Data = new Uint8Array(nBytes);
    for (var nIdx = 0; nIdx < nBytes; nIdx++) {
      ui8Data[nIdx] = sData.charCodeAt(nIdx) & 0xff;
    }
    /* send as ArrayBufferView...: */
    this.send(ui8Data);
  };

  function postImageToFacebook(authToken, filename, mimeType, imageData, message) {
    // this is the multipart/form-data boundary we'll use
    var boundary = '----ThisIsTheBoundary1234567890';
    // let's encode our image file, which is contained in the var
    var formData = '--' + boundary + '\r\n';
    formData += 'Content-Disposition: form-data; name="source"; filename="' + filename + '"\r\n';
    formData += 'Content-Type: ' + mimeType + '\r\n\r\n';
    for (var i = 0; i < imageData.length; ++i) {
      formData += String.fromCharCode(imageData[i] & 0xff);
    }
    formData += '\r\n';
    formData += '--' + boundary + '\r\n';
    formData += 'Content-Disposition: form-data; name="message"\r\n\r\n';
    formData += message + '\r\n';
    formData += '--' + boundary + '--\r\n';

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://graph.facebook.com/me/photos?access_token=' + authToken, true);
    xhr.onload = xhr.onerror = function() {
      console.log(xhr.responseText);
      var result = JSON.parse(xhr.responseText);
      if (!result.error) {
        toastr.success('已成功將課表發佈至您的塗鴉牆上。');
      }
    };
    xhr.setRequestHeader("Content-Type", "multipart/form-data; boundary=" + boundary);
    xhr.sendAsBinary(formData);
  }
});
