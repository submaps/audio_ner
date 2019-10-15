from urllib.parse import urlencode
import speech_recognition as sr
import requests
import os

ifile_path = "data/chunk1.wav"
ofile_path = 'output/chunk1.txt'
r = sr.Recognizer()

with sr.AudioFile(ifile_path) as source:
    audio_data = r.listen(source)
    key = os.environ['GOOGLE_SPEECH_API_KEY']
    url = "https://www.google.com/speech-api/v2/recognize?{}".format(
        urlencode({
        "client": "chromium",
        "lang": 'ru-RU',
        "key": key,
        })
    )
    print('recognition started', ifile_path)
    flac_data = audio_data.get_flac_data(
        convert_rate=None if audio_data.sample_rate >= 8000 else 8000,  # audio samples must be at least 8 kHz
        convert_width=2  # audio samples must be 16-bit
    )
    response = requests.post(url, data=flac_data,
                                  headers={"Content-Type": "audio/x-flac; rate={}".format(audio_data.sample_rate)})
    response_text = response.text
    print('result:', response_text)
    open(ofile_path, 'w', encoding='utf-8').write(response_text)
    print('saved', ofile_path)
