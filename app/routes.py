from flask import render_template, redirect, request, flash, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
from werkzeug import datastructures
#import tone
from app import app
#from PIL import Image
#from micro_api import process_image
import requests
import sys
import json

# Speech to Text
from watson_developer_cloud import SpeechToTextV1
from os.path import join, dirname
from io import BytesIO


face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'
subscription_key = "1edbcc88a7cb4bc481db94d73118f891"
assert subscription_key
headers = {
     'Content-Type': 'application/octet-stream',
     'Ocp-Apim-Subscription-Key': subscription_key,
}
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion'
}
path_to_face_api = '/face/v1.0/detect'

photos = UploadSet('photos', IMAGES)

def process_image(filename):
    result = "../user_uploaded/" + filename
    with open(result, 'rb') as f:
        img_data = f.read()
        #f.save(result)
    try:
        response = requests.post(uri_base + path_to_face_api, data=img_data, headers=headers, params=params)

#print ('Response:')
# json() is a method from the request library that converts
# the json reponse to a python friendly data structure
        faces = response.json()
        return faces
    except Exception as e:
        print('Error:')
        print(e)

app.config['UPLOADED_PHOTOS_DEST'] = 'static'
configure_uploads(app, photos)

speech_to_text = SpeechToTextV1(
    username='00a7563d-48a3-4150-857c-66774523f6f0',
    password='CraD4bMgCQKu',
    url='https://stream.watsonplatform.net/speech-to-text/api'
)

# List of Models
# speech_models = speech_to_text.list_models().get_result()
# print(json.dumps(speech_models, indent=2))

# Download the files to the current directory
# Modify the keywords and file type
files = ['audio-file2.flac']
for file in files:
    with open(join(dirname(__file__), '', file),
                   'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/flac',
            word_alternatives_threshold=0.9,
            keywords=['hack'],
            keywords_threshold=0.5).get_result()
    print(json.dumps(speech_recognition_results["results"][0]["alternatives"][0]["transcript"], indent=2))

# Toner Analyzer
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version='2016-05-19',
    username='a268baec-b85d-4221-8315-bd9d566ac155',
    password='oGzK2sCkyes4',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

text = speech_recognition_results["results"][0]["alternatives"][0]["transcript"]

tone_analysis = tone_analyzer.tone(
    {'text': text},
    'application/json').get_result()
print(json.dumps(tone_analysis["document_tone"]["tone_categories"][0]["tones"], indent=2))

@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not 'image' in request.files:
            flash('Please upload an image')
            return redirect('index')
        else:
            filename = photos.save(request.files['image'])
            faces = process_image(filename)
            faces[0]['faceAttributes']['age'] = round(faces[0]['faceAttributes']['age']);
            print(faces, file = sys.stderr)

            return render_template('analysis.html', faces=faces)
    else:
        return render_template('index.html')
