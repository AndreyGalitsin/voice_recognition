import vosk
from vosk import Model, SpkModel
try:
    from vosk import GpuInit, GpuInstantiate, SetLogLevel
    GpuInit()
    def thread_init():
        GpuInstantiate()
    thread_init()
except: 
    from vosk import SetLogLevel

from wav_separation.Wav_separation import Wav_separation
from vosk_api.speaker_identification import Speaker_identification
from vosk_api.speech_to_text import speech_to_text
from scipy.io import wavfile
import datetime
import os

class Voice_module:
    def __init__(self, session_number=1):
        model_path = "./vosk_api/model"
        spk_model_path = "./vosk_api/model-spk"

        self.model = Model(model_path)
        self.spk_model = spk_model = SpkModel(spk_model_path)



        path_to_session = '/home/ssedunov/voice_recognition/sound/session_' + str(session_number)+'/'

        self.path_to_stereo_wav = path_to_session + 'stereo_wavs/hdcam.wav'
        self.path_to_voiceprint = path_to_session + "voiceprint/identification_phrase.wav"
        self.path_to_save_separated_wavs = path_to_session + 'separated_wavs/'
        self.path_to_save_right_speaker_wav = path_to_session + 'right_speaker'

    def separate_wav(self):
        wav_separation = Wav_separation()
        mics_signals, separated_signals, fs = wav_separation.main(self.path_to_stereo_wav)

        nof_speakers = len(separated_signals)
        separated_wavs = []
        for num, speaker in enumerate(range(nof_speakers), 1):
            wav_name = 'spk_' + str(num) + '.wav'
            path_to_wav = self.path_to_save_separated_wavs + wav_name
            separated_wavs.append(path_to_wav)
            audio = separated_signals[speaker]
            wav_separation.save_wav(path_to_wav, fs, audio)

        return separated_wavs, fs

    def check_extension(self):
        if os.path.basename(self.path_to_stereo_wav).split('.')[-1] != 'wav':
            self.path_to_stereo_wav = wav_separation.any_exp_to_wav(self.path_to_stereo_wav)
        else: pass

        if os.path.basename(self.path_to_voiceprint).split('.')[-1] != 'wav':
            self.path_to_voiceprint = wav_separation.any_exp_to_wav(self.path_to_stereo_wav)
        else: pass

    def main(self):
        sep_start_time = datetime.datetime.now()
        speaker_identification = Speaker_identification()
        self.check_extension()
        separated_wavs, fs = self.separate_wav()
        sep_finish_time = datetime.datetime.now()

        distances = []
        dis_start_time = datetime.datetime.now()
        for sep_wav in separated_wavs:
            distance = speaker_identification.compare_with_voiceprint(sep_wav, self.path_to_voiceprint, self.model, self.spk_model)            
            distances.append(distance)


        dist, idx = min((dist, idx) for (idx, dist) in enumerate(distances))

        right_speaker_wav_path = separated_wavs[idx]
        dis_finish_time = datetime.datetime.now()

        speech_to_text_start_time = datetime.datetime.now()
        final_res = speech_to_text(right_speaker_wav_path, self.model)
        speech_to_text_finish_time = datetime.datetime.now()

        print()
        print('separated_wavs', separated_wavs)
        print('distances', distances)
        print()
        print('Separation time', sep_finish_time-sep_start_time)
        print('Distance comparison time', dis_finish_time-dis_start_time)
        print('Speech to text time', speech_to_text_finish_time-speech_to_text_start_time)

        return final_res

if __name__ == "__main__":
    t1 = datetime.datetime.now()
    SetLogLevel(0)
    voice_module = Voice_module(1)
    
    final_res = voice_module.main()
    t2 = datetime.datetime.now()
    print('Speaker said: ', final_res)
    
    
    print()
    print('Full time', t2-t1)