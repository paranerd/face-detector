# https://github.com/log0/video_streaming_with_flask_example

import os, time, json
import base64
from werkzeug.utils import secure_filename
from multiprocessing import Process
from flask import Flask, render_template, Response, send_file, stream_with_context, redirect, url_for, flash, request
from face_detector import FaceDetector

UPLOAD_FOLDER = './tmp'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setup detectors
fd = FaceDetector()
fd.start()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
	if request.method == 'POST':
		# Check if file exists
		if 'file' not in request.files:
			return error(400, 'No file selected')

		file = request.files['file']

		# User hit submit without selecting a file
		if file.filename == '':
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(path)
			count, image = fd.detectFromImage(path)
			os.remove(path)

			if count > 0:
				return json.dumps({'count': count, 'data': base64.b64encode(image).decode('utf-8')})
			else:
				return error(404, "No face found")

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def error(code, msg=""):
	return Response(json.dumps(msg), status=code, mimetype='application/json')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
