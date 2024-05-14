import pyotp
import qrcode
from PIL import Image
import sys
import time

# ONE TIME PASSWORD GENERATOR -------------------------------------------------------------------------------------
# This script generates a QR code for a given secret and user, and then prints the current OTP for the given secret.
# The QR code can be scanned by an authenticator app, such as Google Authenticator, to generate OTPs.
# The script uses the pyotp library to generate TOTP (Time-based One-Time Password) codes.
# The QR code is generated using the qrcode library.
# Source for TOTP: https://datatracker.ietf.org/doc/html/rfc6238#section-4 , https://pyotp.readthedocs.io/en/latest/

def generate_qr(secret, user):
    """
    Generates a QR code for the given secret and user.
    Saves the QR code as a PNG file.
    """
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user, issuer_name='OTP Test')
    image = qrcode.make(uri)
    image.save('qr.png')
    print('QR code saved as qr.png')

def get_otp(secret):
    """
    Returns the current OTP for the given secret.
    Uses 30 second TOTP codes.
    """
    totp = pyotp.TOTP(secret)
    while True:
        print("Current OTP: ", totp.now())
        time.sleep(30)

if __name__ == "__main__":
    # example secret
    secret = 'VERY$ECRET'
    user = 'user@users.com'

    if len(sys.argv) != 2:
        print("ERROR - Usage: python otp.py [generate | get]")
        sys.exit(1)

    # generate QR code, save
    if sys.argv[1] == '--generate-qr':
        generate_qr(secret, user)

    # prinnt the current OTP, 30 second loop
    elif sys.argv[1] == '--get-otp':
        get_otp(secret)
    else:
        print("ERROR - Usage: python otp.py [--generate-qr | --get-otp]")
        sys.exit(1)