import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from natasha import NamesExtractor
import pandas as pd


def convert_mp3(ifile_path):
    if ".mp3" in ifile_path:
        print("mp3 detected")
        sound = AudioSegment.from_mp3(ifile_path)
        print(ifile_path)
        ifile_path = ifile_path.replace(".mp3", ".wav")
        sound.export(ifile_path, format="wav")
        print("file exported", ifile_path)


def split_audio(ifile_path, odir):
    os.makedirs(odir, exist_ok=True)
    sound = AudioSegment.from_wav(ifile_path)
    for i, part in enumerate(split_on_silence(sound)):
        part.export(f"{odir}/{i}.wav", format="wav")


def trim_sample(ifile_path, ofile_path, start_min, start_sec, end_min, end_sec):
    # Time to miliseconds
    startTime = start_min * 60 * 1000 + start_sec * 1000
    endTime = end_min * 60 * 1000 + end_sec * 1000
    song = AudioSegment.from_mp3(ifile_path)
    extract = song[startTime:endTime]
    extract.export(ofile_path, format="wav")


def main():
    r = sr.Recognizer()
    database_path = "data/audio_database.csv"
    database = pd.DataFrame()
    print("found database", database.columns)

    ifile_sample_path = f"data/chunk1.wav"
    if len(database) == 0 or ifile_sample_path not in database['audio_file'].unique():
        print("recognize in google")
        with sr.AudioFile(ifile_sample_path) as source:
            audio = r.listen(source)
            text = r.recognize_google(audio, language="ru-RU")
            database = database.append({"audio_file": ifile_sample_path, "text": text},
                                        ignore_index=True)
            print(database.values)
            database.to_csv(database_path, mode='a', sep='\t', header=None, index=False)
    else:
        print("found in database")
        text = database.query("audio_file == @ifile_sample_path").values[0]
        print(text)

    print(ifile_sample_path, text)
    get_ner("20 июня 2017  Яков лежал на сене в Неаполе, когда подошел Абрамова Иван и сказал: п* работать!")
    get_ner("20 июня 2017 года Яков лежал на сене в неаполе, когда подошел Абрамов Иван и сказал: п* работать!")


def get_microphone_sample(r):
    with sr.Microphone() as source:
        print("Скажите что-нибудь")
        audio = r.listen(source)
        return audio


def get_ner(text):
    print("text for ner:")
    print(text)
    extractor = NamesExtractor()
    matches = extractor(text)
    print("found ner:", len(matches))
    for match in matches:
        print(match.span, match.fact)


if __name__ == '__main__':
    main()
