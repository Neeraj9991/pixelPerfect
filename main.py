import numpy as np
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Apply grayscale effect
def apply_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply sepia effect
def apply_sepia(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia_image = cv2.transform(img, kernel)
    return sepia_image

# Apply blur filter
def apply_blur(img):
    blurred_image = cv2.GaussianBlur(img, (15, 15), 0)
    return blurred_image

# Apply edge detection filter
def apply_edge_detection(img):
    edges = cv2.Canny(img, 100, 200)
    return edges

# Apply custom filter
def apply_custom_filter(img):
    # Define the custom filter kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    filtered_image = cv2.filter2D(img, -1, kernel)
    return filtered_image


def processImage(filename, operation):
    print(f'The filename is {filename}')
    print(f'The operation is {operation}')

    img = cv2.imread(f'uploads/{filename}')

    match operation:
        case "cgray":
            processed_image = apply_grayscale(img)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, processed_image)
            return newFilename
        case "csepia":
            processed_image = apply_sepia(img)
            newFilename = f"static/{filename.split('.')[0]}_sepia.jpg"
            cv2.imwrite(newFilename, processed_image)
            return newFilename
        case "cblur":
            processed_image = apply_blur(img)
            newFilename = f"static/{filename.split('.')[0]}_blur.jpg"
            cv2.imwrite(newFilename, processed_image)
            return newFilename
        case "cedge":
            processed_image = apply_edge_detection(img)
            newFilename = f"static/{filename.split('.')[0]}_edge.jpg"
            cv2.imwrite(newFilename, processed_image)
            return newFilename
        case "ccustom":
            processed_image = apply_custom_filter(img)
            newFilename = f"static/{filename.split('.')[0]}_custom.jpg"
            cv2.imwrite(newFilename, processed_image)
            return newFilename



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('/index.html')


@app.route('/edit', methods=["GET", "POST"])
def edit():

    if request.method == 'POST':
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "Error : No file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            new = processImage(filename, operation)
            flash(
                f"Your Image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template('index.html')

    return render_template('index.html')


app.run(debug=True)
