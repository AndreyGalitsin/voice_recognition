
#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SpkModel
import sys
import wave
import json
import os
import numpy as np
from pydub import AudioSegment

import pyaudio
import wave

class Make_print:
    def __init__(self):
        self.CHUNK = 4000
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        
        self.model_path = "./vosk_api/model"
        self.spk_model_path = "./vosk_api/model-spk"

    def create_print(self, print_path="./sound/Andrey/identification_phrase.wav"):
        WAVE_OUTPUT_FILENAME = print_path
        #p = pyaudio.PyAudio()
        
        model_path = self.model_path
        spk_model_path = self.spk_model_path

        wf = wave.open(WAVE_OUTPUT_FILENAME, "rb")

        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print ("Audio file must be WAV format mono PCM.")
            exit (1)

        # Large vocabulary free form recognition
        model = Model(model_path)
        spk_model = SpkModel(spk_model_path)
        rec = KaldiRecognizer(model, spk_model, wf.getframerate())
        
        voice_print = []
        text = []
        while 1:
            data = wf.readframes(1000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                text.append(res['text'])
                voice_print.append(res['spk'])

        voice_print = self.fix_print(voice_print)
        
        return voice_print


    def fix_print(self, voice_print):
        if len(voice_print) != 1:
            voice_print = voice_print[1]
        else:
            voice_print = voice_print[0]

        return voice_print

'''
if __name__ == "__main__":
    make_print = Make_print()

    print_path="./sound/Andrey/ex_1.wav"
    voice_print = make_print.create_print(print_path)

    print(voice_print)
'''