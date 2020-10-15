from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json



def speech_to_text(input_path, model):
    '''
    if not os.path.exists("./vosk_api/model"):
        print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
        exit (1)
    '''
    wf = wave.open(input_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    #model = Model("./vosk_api/model")
    rec = KaldiRecognizer(model, wf.getframerate())
    final_res = []
    while True:
        
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = rec.Result()
            res = json.loads(res)['text']
            final_res.append(res)
    return final_res
    
'''
if __name__ == "__main__":
    input_path = './sound/spk_1.wav'
    final_res = speech_to_text(input_path)

    print('Speaker said: ', final_res)
'''
