
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import sys
import numpy as np

def distance_to_camera(knownWidth,focalLength, perWidth):

	return (knownWidth * focalLength) / perWidth

KNOWN_DISTANCE = 60.0    #Distance from camera to marker
KNOWN_WIDTH = 6.3        #original width of marker


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to detect")
args = vars(ap.parse_args())

# define names of 7x7 aruco
ARUCO_DICT = {
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
	sys.exit(0)

# Loading the ArUco dictionary
print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

#Video Stream Settings
print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
time.sleep(2.0)

frame = cv2.imread(r'C:\Users\asus\Desktop\pycharm\pythonProject1\GP\detection\cameracalibration.jpeg')
x = imutils.resize(frame, width=1000)


# detect ArUco markers in the video stream
(corners, ids, rejected) = cv2.aruco.detectMarkers(frame,arucoDict, parameters=arucoParams)

# verify *at least* one ArUco marker was detected
if len(corners) > 0:
	# flatten the ArUco IDs list
	ids = ids.flatten()

	# loop over the detected ArUCo corners
	for (markerCorner, markerID) in zip(corners,ids):
		# extract the marker corners (which are always returned in top-left, top-right, bottom-right, and bottom-left order)
		corners = markerCorner.reshape((4, 2))
		(topLeft, topRight, bottomRight, bottomLeft) = corners

		# convert each of the (x, y)-coordinate pairs to integers
		topRight = (int(topRight[0]), int(topRight[1]))
		bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
		bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
		topLeft = (int(topLeft[0]), int(topLeft[1]))

		font = cv2.FONT_HERSHEY_PLAIN

		x_max = int(topRight[0])
		x_min = int(topRight[0])

		if (int(bottomRight[0]) > x_max):
			x_max = int(bottomRight[0])
		elif (int(bottomLeft[0]) > x_max):
			x_max = int(bottomLeft[0])
		elif (int(topLeft[0]) > x_max):
			x_max = int(topLeft[0])

		if (int(bottomRight[0]) < x_min):
			x_min = int(bottomRight[0])
		elif (int(bottomLeft[0]) < x_min):
			x_min = int(bottomLeft[0])
		elif (int(topLeft[0]) < x_min):
			x_min = int(topLeft[0])

		initialWidth = x_max - x_min


		# draw the bounding box of the ArUCo detection
		cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
		cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
		cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
		cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

		break

focalLength = (initialWidth * KNOWN_DISTANCE) / KNOWN_WIDTH



while True:

	frame = vs.read()
	frame = imutils.resize(frame, width=1000)


	# detect ArUco markers in the input frame
	(corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()

		for (markerCorner, markerID) in zip(corners, ids):
			# returned in top-left, top-right, bottom-right, and bottom-left order)
			corners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners

			# convert each of the (x, y)-coordinate pairs to integers
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			x_mean = int((int(topRight[0]) + int(bottomRight[0]) + int(bottomLeft[0]) + int(topLeft[0]))/4)
			y_mean = int((int(topRight[1]) + int(bottomRight[1]) + int(bottomLeft[1]) + int(topLeft[1]))/4)

			font = cv2.FONT_HERSHEY_PLAIN

			x_max = int(topRight[0])
			x_min = int(topRight[0])

			if(int(bottomRight[0]) > x_max):
				x_max = int(bottomRight[0])
			elif(int(bottomLeft[0]) > x_max):
				x_max = int(bottomLeft[0])
			elif(int(topLeft[0]) > x_max):
				x_max = int(topLeft[0])

			if(int(bottomRight[0]) < x_min):
				x_min = int(bottomRight[0])
			elif(int(bottomLeft[0]) < x_min):
				x_min = int(bottomLeft[0])
			elif(int(topLeft[0]) < x_min):
				x_min = int(topLeft[0])

			w = x_max - x_min



			if (w != 0):
				inches = distance_to_camera(KNOWN_WIDTH, focalLength, w)
				cv2.putText(frame, "%.2fcm" % (inches),
							(x_mean, y_mean), cv2.FONT_HERSHEY_SIMPLEX,
							0.6, (0, 0, 255), 2)

				# draw the bounding box of the ArUCo detection
				cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
				cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
				cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
				cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)



				# compute and draw the center (x, y)-coordinates of the ArUco marker
				cX = int((topLeft[0] + bottomRight[0]) / 2.0)
				cY = int((topLeft[1] + bottomRight[1]) / 2.0)
				center = (cX,cY)
				radius = 5
				cv2.circle(frame, center, radius, (0, 255, 255), -1)
				print("Center coordinate of marker: " + str(center))

	# show the output frame


	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

cv2.destroyAllWindows()