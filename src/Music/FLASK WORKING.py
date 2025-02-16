
# A very simple Flask Hello World app for you to get started with...
from svgpathtools import svg2paths2
import numpy as np
import soundfile as sf
import os
from flask import Flask, flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename
import sys
import io

UPLOAD_FOLDER = '/home/musiti/mysite/svgsuploaded'
ALLOWED_EXTENSIONS = {'svg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "AudioGrafitti"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return "failed"
        file = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "failed2"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            paths, attributes, svg_attributes = svg2paths2(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            total = 0
            for i in range(len(paths)):
                mypath = paths[i]
                total = total + mypath.length()
            print ("total = ", total)
            vel = total / 2000
            print ("Velocity = ", int(vel))
            arr = np.zeros((0,2))
            for i in range(len(paths)):
                curpath = paths[i]
                for j in np.arange(0, mypath.length(), vel):
                    arr = np.append(arr,[[(curpath.point(j/mypath.length()).real - 512)/512,(512 - curpath.point(j/mypath.length()).imag)/512]], axis = 0)
            
            sf.write(os.path.join(app.config['UPLOAD_FOLDER'], filename) + ".wav", arr, 48000)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) + ".wav"
            return_data = io.BytesIO()
            with open(file_path, 'rb') as fo:
                return_data.write(fo.read())

            return_data.seek(0)

            os.remove(file_path)

            return send_file(return_data, mimetype='audio/wavf',
                             attachment_filename='Musiti_Stereo.wav')

    else:
        return render_template('index.html')
    return redirect(request.url)



