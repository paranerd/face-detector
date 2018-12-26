import sys, getopt
import cv2
import threading

class FaceDetector(threading.Thread):
	def __init__(self, doDisplay=False):
		threading.Thread.__init__(self)

		self.doDisplay = doDisplay

		# Create the haar cascade
		self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

	def __del__(self):
		if self.doDisplay:
			cv2.destroyAllWindows()

	def detectFromImage(self, imagePath):
		# Read image from file
		image = cv2.imread(imagePath)
		count, frame = self.findFace(image)

		if self.doDisplay:
			cv2.waitKey(0)

		retval, buffer = cv2.imencode('.jpg', frame)
		return count, buffer

	def detectFromCam(self):
		try:
			# Read image from webcam
			self.videoCapture = cv2.VideoCapture(0)

			while True:
				# Capture frame-by-frame
				ret, frame = self.videoCapture.read()
				self.findFace(frame)

				if self.doDisplay and cv2.waitKey(1) & 0xFF == ord('q'):
					break
		finally:
			self.videoCapture.release()

	def findFace(self, frame):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = self.faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE
		)

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

		if self.doDisplay:
			# Display the resulting frame
			cv2.namedWindow('face', cv2.WINDOW_NORMAL)
			cv2.resizeWindow('face', 600, 600)
			cv2.imshow('face', frame)

		return len(faces), frame

if __name__ == "__main__":
	args = sys.argv[1:]
	source = None
	doDisplay = False

	try:
		opts, args = getopt.getopt(args, "hs:d",["source=", "display"])
	except getopt.GetoptError:
		print('python3 face_detector.py -s <source>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('python3 face_detector.py -s <source>')
			sys.exit()
		elif opt in ("-s", "--source"):
			source = arg.strip()
		elif opt in ("-d", "--display"):
			doDisplay = True

	fd = FaceDetector(doDisplay=doDisplay)

	if source:
		fd.detectFromImage(source)
	else:
		fd.detectFromCam()
