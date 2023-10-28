from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model

app= Flask(__name__)
model = load_model('model.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dog')
def dog():
    return render_template('dog.html')

@app.route('/cat')
def cat():
    return render_template('cat.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        image = request.files['image']
        image = request.files['image']
        if image.filename != '':
            image.save(os.path.join('uploads', image.filename))

        img = cv2.imread(str(os.path.join('uploads', image.filename)))
        resized_img = cv2.resize(img, (200,200))
        resized_img = np.array(resized_img)
        resized_img = resized_img/255
        resized_img = resized_img.reshape(1,200,200,3)

        prediction = model.predict(resized_img)[0][0]
        output = ""
        if prediction >= 0.5:
            output="dog"
        else:
            output="cat"
    return redirect(url_for(output))

if __name__=='__main__':
    app.run(debug=True)
