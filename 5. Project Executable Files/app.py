import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import model_from_json
from flask import Flask, redirect, request, render_template, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
app = Flask(__name__)

global curr
curr = {"description": "Upload an image and click predict", "prediction_text": "None", "file": None}

model = load_model('model.h5')
def get_prediction(image_path,labels):
    img = load_img(image_path, target_size=(255, 255))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    predictions = model.predict(x, verbose=0)


    return labels[predictions.argmax()]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediction_page')
def prediction_page():
    global curr
    return render_template('prediction_page.html', text=curr["prediction_text"], description=curr["description"])

@app.route('/predict', methods=['POST'])
def predict():
    # Load and preprocess the image

    return jsonify(success=True)

@app.route('/render', methods=['POST'])
def render():
    global curr
    f = request.files['image']
    if f.filename == '':
        return jsonify(success=False, message="No selected file"), 400

    basepath = os.path.dirname(__file__)
    upload_folder = os.path.join(basepath, 'static', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filepath = os.path.join(upload_folder, secure_filename(f.filename))
    f.save(filepath)
    curr["file"] = secure_filename(f.filename)

    try:


        index = ['cables', 'case', 'cpu', 'gpu', 'hdd', 'headset', 'keyboard', 'microphone', 'monitor',
                 'motherboard', 'mouse', 'ram', 'speakers', 'webcam']
        a = get_prediction(filepath, index)
        curr["prediction_text"] = "The predicted item is: " + a

        description = {
            "cables": "Cables are essential components used to connect various hardware devices in a computer setup, including power cables, data cables, and peripheral cables.",
            "case": "The case, or chassis, houses and protects the computer's internal components, providing structure and cooling for the system.",
            "cpu": "The CPU (Central Processing Unit) is the brain of the computer, responsible for processing instructions and managing the operations of other components.",
            "gpu": "The GPU (Graphics Processing Unit) renders images and videos for display, handling tasks related to graphics and visual output.",
            "hdd": "The HDD (Hard Disk Drive) is a storage device used to store and retrieve digital information using magnetic storage.",
            "headset": "A headset combines headphones and a microphone, allowing for audio playback and voice communication, often used in gaming and telecommunication.",
            "keyboard": "The keyboard is an input device used to type and interact with a computer, consisting of keys for letters, numbers, and functions.",
            "microphone": "A microphone captures audio input, allowing users to record sound or communicate via voice.",
            "monitor": "The monitor is a display screen that shows the visual output from the computer, allowing users to interact with the graphical user interface.",
            "motherboard": "The motherboard is the main circuit board that connects all components of a computer, including the CPU, memory, and peripheral devices.",
            "mouse": "The mouse is a pointing device that allows users to interact with the computer's graphical user interface by moving a cursor on the screen.",
            "ram": "RAM (Random Access Memory) is a type of computer memory that stores data temporarily, allowing for fast access and efficient multitasking.",
            "speakers": "Speakers output audio from the computer, allowing users to hear sound from applications, media, and games.",
            "webcam": "A webcam captures video input, allowing users to participate in video calls, record videos, and take photos."
        }

        curr["description"] = description[a]
        print(curr)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
