# ONE TIME PASSWORD GENERATOR

### DESCRIPTION 
 - This project implements a TOTP (Time-based One-Time Password) generator. It is a command line application that generates a 6-digit OTP based on the current time and a secret key. The OTP is valid for 30 seconds and will match output on a Google Authenticator app.

### REQUIREMENTS 
- Python 3+
- libraries: pyotp, qrcode, pillow

### INSTALLATION 
- Recommended to use a venv
- Install the required libraries using pip: `pip install pyotp qrcode[pil]`

### USAGE 
1. To generate a QR code, run the script with the "--generate-qr" flag like so:
       `python otp.py --generate-qr`
       This will generate a QR code that can be scanned by a Google Authenticator app. The QR code will be saved as a PNG file in the same directory as the script.

2. Scan the QR code with a Google Authenticator app on your phone or other device. This will add a new account to the app with the secret key.

3. To get the current OTP, run the script with "--get-otp" flag like so:
       `python otp.py --get-otp`
       This will generate a 6-digit OTP based on the current time and the secret key. The OTP will be printed to the console, and should match the output on a Google Authenticator app.

### NOTES 
- You can change the secret key and email in the script to generate your own keys. It is located on lines 36 and 37 - underneath the "example" comment

### SOURCES 
- https://pyotp.readthedocs.io/en/latest/
- https://tools.ietf.org/html/rfc6238
- all credit to library creators
