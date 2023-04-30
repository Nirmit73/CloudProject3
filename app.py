from flask import Flask, request, render_template_string, redirect, url_for
import base64
import cv2
import numpy as np
import os 
from werkzeug.utils import secure_filename

app = Flask(__name__)

def img2sketch(img, k_size):
    
    # Convert to Grey Image
    grey_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert Image
    invert_img=cv2.bitwise_not(grey_img)
    #invert_img=255-grey_img

    # Blur image
    blur_img=cv2.GaussianBlur(invert_img, (k_size,k_size),0)

    # Invert Blurred Image
    invblur_img=cv2.bitwise_not(blur_img)
    #invblur_img=255-blur_img

    # Sketch Image
    sketch_img=cv2.divide(grey_img,invblur_img, scale=256.0)

    # Save Sketch 
    return (sketch_img)


@app.route('/')
def index():
    html = '''
        <html>
            <body>
                <form method="POST" enctype="multipart/form-data">
                    <input type="file" name="image"/>
                    <input type="submit" value="Upload"/>
                </form>
            </body>
        </html>
    '''
    return html

@app.route('/', methods=['POST'])
def upload():
    f = request.files['image']
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
    f.save(file_path)
    
    image = cv2.imread(file_path)
    image= img2sketch(image, 7)
    _, img_encoded = cv2.imencode('.jpg', image)
    image_b64 = base64.b64encode(img_encoded).decode('utf-8')

    html = f'''
        <html>
            <body>
                <img src="data:image/png;base64,{image_b64}">
            </body>
        </html>
    '''
    return html

if __name__ == '__main__':
    app.run(debug=False)
