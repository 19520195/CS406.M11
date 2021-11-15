import os
import cv2
from flask import flash, Flask, request, redirect, send_file, url_for, render_template, make_response
from werkzeug.utils import secure_filename
from censorLicensePalateAPI import *
import hashlib
from datetime import datetime
from config import *

if CFG_MODEL == 'yolo':
    from modelYOLO import *
    model = modelYOLO()
else:
    from modelFasterRCNN import *
    model = modelFasterRCNN()
    
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
from flask_ngrok import run_with_ngrok
run_with_ngrok(app)
# if CFG_API_DEVICE == 'ngrok':
    # from flask_ngrok import run_with_ngrok
    # run_with_ngrok(app)
    
app.secret_key = 'CS406.M11'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def convertFileName(fileName):
    return hashlib.md5((str(datetime.now().time()) + "_" + fileName).encode()).hexdigest() + ".jpg"

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
    response = make_response(render_template('ultralytics.html'))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = convertFileName(secure_filename(file.filename))
        path_save = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_save)
        flash('Image successfully uploaded and displayed below')
        

        image_res = None
        image = cv2.imread(path_save)
        list_coors = model.predict(image)
        typeBlur = int(request.form['typeBlur'])
        
        
        
        
        if typeBlur == 6: # Replace Image
            file_replace = request.files['imageReplace']
            filename_replace = convertFileName(secure_filename(file_replace.filename))
            path_save_replace = os.path.join(app.config['UPLOAD_FOLDER'], filename_replace)
            file_replace.save(path_save_replace)
            image_replace = cv2.imread(path_save_replace)
            imageResult = convertImage(image, list_coors).replaceImage(image_replace)
        else:
            kernelSize = int(request.form['kernelSize'])
            if typeBlur == 1: # averageBlur
                imageResult = convertImage(image, list_coors).averageBlur(kernelSize)
            elif typeBlur == 2: # gaussianBlur
                imageResult = convertImage(image, list_coors).gaussianBlur(kernelSize)
            elif typeBlur == 3: # medianBlur
                imageResult = convertImage(image, list_coors).medianBlur(kernelSize)            
            elif typeBlur == 4: # eightBitsBlur
                kernelDepth = int(request.form['kernelDepth'])
                imageResult = convertImage(image, list_coors).eightBitsBlur(kernelSize, kernelDepth)
            elif typeBlur == 5: # bilateralBlur
                imageResult = convertImage(image, list_coors).GaussianBlur(kernelSize)  ### Thay cho nay
                
        path_save_res = os.path.join(app.config['UPLOAD_FOLDER'], "res_" + filename)
        cv2.imwrite(path_save_res, imageResult)
        return render_template('ultralytics.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/download/<filename>')
def downloadFile(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == "__main__":
    app.run()