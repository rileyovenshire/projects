# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Date: 2/1/24
# Description: A Flask-based image recolorization tool for CS 361 - takes an image and allows a user to customize it with their own
#   recolorization options. Will be implemented with a palette selection tool that is a built-in microservice.
#  This is the main file for the Flask app, and will be used to run the server and handle requests.
#  See the readme for information on sources, usage, and more.

from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# ----------------------------------------------------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------------------------------------------------
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ----------------------------------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------
def allowed_file(filename):
    """
    Check if a file is allowed based on its extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ----------------------------------------------------------------------------------------------------------------
# ROUTES
# ----------------------------------------------------------------------------------------------------------------

# main page
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main page route. Handles file uploads and displays images.
    """
    if request.method == 'POST':
        file = request.files.get('file')

        # check file is not empty and allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # fetch list of uploaded images
    images = [file for file in os.listdir(UPLOAD_FOLDER) if allowed_file(file)]
    return render_template('index.html', images=images)


# file upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded files directly.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# delete image
@app.route('/delete/<filename>', methods=['POST'])
def delete_image(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"success": True, "message": "Image deleted successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Image not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# recolorize route
@app.route('/recolorize', methods=['POST'])
def recolor(filename):
    """
        Recolorize a selected image.
        """
    # Zhang algorithm - see readme for sources


# ----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
