$("#upload").on('click', function(e) {
	$(this).find('input').trigger('click');
});

$(".upload-input").on('click', function(e) {
	e.stopPropagation();
});

$("#upload input").on('change', function(e) {
	upload(this.files[0])
});

function upload(file) {
		var fd = new FormData();
		var xhr = new XMLHttpRequest();

		// Register load callback
		xhr.addEventListener("load", function() {
			let res = JSON.parse(xhr.responseText);
			$("#upload").prop('disabled', false);
			$("#upload i").addClass("hidden");
			showImage(res.data);
			showMessage(res.count + " face(s) found");
		});

		// Register end callback
		xhr.onreadystatechange = function() {
			if (xhr.readyState == 4 && xhr.status != 200) {
				showMessage(JSON.parse(xhr.response))
			}
		}

		// Register start callback
		xhr.onloadstart = function(ev) {
			$("#upload").prop('disabled', true);
			$("#upload i").removeClass("hidden");
		}

		// Execute request
		xhr.open("POST", "/detect", true);
		fd.append('file', file);
		xhr.send(fd);
}

function showImage(base64Image) {
	let img = new Image()
	img.src = 'data:image/jpeg;base64,' + base64Image;

	img.onload = function() {
		let img_scaled = scale(this);
		img_scaled.className = "video";
		$("#result").empty().append(img_scaled);
	}
}

function scale(img) {
	let scale = Math.max(img.height / 480, img.width / 640);

	img.width = img.width / scale;
	img.height = img.height / scale;

	return img;
}

function showMessage(msg) {
	$("#message").text(msg);
}
