
#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SpkModel
import sys
import wave
import json
import os
import numpy as np
from pydub import AudioSegment
from make_print import Make_print


class Speaker_identification:
    def __init__(self):
        self.model_path = "model"
        self.spk_model_path = "model-spk"
        self.warnings()

    def warnings(self):
        if not os.path.exists(self.model_path):
            print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as {} in the current folder.".format(self.model_path))
            exit (1)

        if not os.path.exists(self.spk_model_path):
            print ("Please download the speaker model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as {} in the current folder.".format(self.spk_model_path))
            exit (1)

    def cosine_dist(self, x, y):
        nx = np.array(x)
        ny = np.array(y)
        return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

    def compare_with_voiceprint(self, path_to_test_wav, path_to_voiceprint):

        wf = wave.open(path_to_test_wav, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print ("Audio file must be WAV format mono PCM.")
            exit (1)

        model = Model(self.model_path)
        spk_model = SpkModel(self.spk_model_path)
        rec = KaldiRecognizer(model, spk_model, wf.getframerate())
        res = json.loads(rec.Result())

        make_print = Make_print()
        voice_print = make_print.create_print(path_to_voiceprint)

        while True:
            data = wf.readframes(1000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                arr = []
                for i in range(len(res['result'])):
                    word_pair = [res['result'][i]['conf'], res['result'][i]['word']]
                    arr.append(word_pair)

                distance = self.cosine_dist(voice_print, res['spk'])
                return distance

if __name__ == "__main__":
    speaker_identification = Speaker_identification()

    path_to_test_wav = "./sound/Andrey/ex_1.wav"
    path_to_voiceprint = "./sound/Andrey/identification_phrase.wav"

    distance = speaker_identification.compare_with_voiceprint(path_to_test_wav, path_to_voiceprint)

    print(distance)


    