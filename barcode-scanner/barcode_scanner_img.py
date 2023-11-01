# Author: Riley Ovenshire
# Source: https://pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
# Description: Single image barcode scanner.

from pyzbar import pyzbar
import argparse
import cv2

# Argument Parser -----------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
args = vars(ap.parse_args())

# Load image ----------------------------------------------------------------------------------
image = cv2.imread(args["image"])
barcode_list = pyzbar.decode(image)

# Loop over detected barcodes -----------------------------------------------------------------
for barcode in barcode_list:
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x,y), (x+w, y+h), (0, 0, 255), 2)

    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

cv2.imshow("Image", image)
cv2.waitKey(0)

