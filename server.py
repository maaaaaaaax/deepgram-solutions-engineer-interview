from flask import Flask, request, redirect, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from os import walk
import librosa
import requests
import wave
import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/Users/maxwiederholt/Desktop/deepgram-homework-assignment/assets'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/post', methods=['POST'])
def hello():
    file = request.files['audio_file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

    url = "https://brain.deepgram.com/v2/listen"

    with open('/Users/maxwiederholt/Desktop/deepgram-homework-assignment/assets/guidance.wav', 'rb') as f:
        payload=f
        headers = {
        'Content-Type': 'audio/wav',
        'Authorization': 'Email Max Wiederholt at max.wiederholt@gmail.com for the API key to place here'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        transcript = response.text
        transcript_json = json.loads(transcript)
        print(transcript_json["results"]["channels"][0]["alternatives"][0]["transcript"])

    return redirect("/")

@app.route("/download/<file_name>")
def print_name(file_name):
    if os.path.isfile('./assets/' + file_name):
        response = send_from_directory(app.config['UPLOAD_FOLDER'], file_name)
        return response
    else:
        return "<p>Hello, World!</p>"

# Return a list of audio files matching a query like http://localhost/list?​maxduration=300
@app.route("/list")
def list_files():
    if "maxduration" in request.args:
        results = []
        filenames = next(walk(app.config['UPLOAD_FOLDER']), (None, None, []))[2]  # [] if no file
        filenames.remove(".DS_Store")
        for file in filenames:
            duration = librosa.get_duration(filename=("assets/" + file))
            if duration <= 300.0:
                result = {
                    "name": file,
                    "duration": duration
                }
                results.append(result)
    return jsonify(results)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"