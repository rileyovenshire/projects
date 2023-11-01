# Author: Riley Ovenshire
# Source: https://pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
# Description: Real time video barcode scanner.

from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

# Initialize video stream, start camera sensor
print("[INFO] Starting video stream...")
stream = VideoStream(src=0).start()
time.sleep(2.0)

# open CSV output for writing
csv = open("output", "w")
codes = set()

# loop frames from video
while True:
    frame = stream.read()
    frame = imutils.resize(frame, width=400)

    # find barcodes in frame and decode
    barcodes = pyzbar.decode(frame)

    # loop over detected barcodes
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # if barcode not in CSV, write to CSV and update set
        if barcodeData not in codes:
            csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))
            csv.flush()
            codes.add(barcodeData)

    # show output frame
    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    # if ESC key pressed, break from loop
    if key == 27:
        break

# close CSV file and cleanup
print("[INFO] Cleaning up...")
csv.close()
cv2.destroyAllWindows()
stream.stop()

