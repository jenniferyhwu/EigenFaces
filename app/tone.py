import json

# Speech to Text 
from watson_developer_cloud import SpeechToTextV1
from os.path import join, dirname

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
