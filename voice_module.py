from wav_separation.Wav_separation import Wav_separation
from vosk_api.make_print import Make_print
from vosk_api.speaker_identification import Speaker_identification
from vosk_api.speech_to_text import speech_to_text
from scipy.io import wavfile
import datetime

class Voice_module:
    def __init__(self, session_number=1):

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

    def main(self):
        speaker_identification = Speaker_identification()
        
        separated_wavs, fs = self.separate_wav()
        
        
        distances = []
        
        for sep_wav in separated_wavs:
            
            distance = speaker_identification.compare_with_voiceprint(sep_wav, self.path_to_voiceprint)            
            distances.append(distance)

        dist, idx = min((dist, idx) for (idx, dist) in enumerate(distances))

        right_speaker_wav_path = separated_wavs[idx]

        final_res = speech_to_text(right_speaker_wav_path)

        print()
        print('separated_wavs', separated_wavs)
        print('distances', distances)
        print()

        return final_res
        




if __name__ == "__main__":
    t1 = datetime.datetime.now()
    voice_module = Voice_module(1)
    final_res = voice_module.main()
    t2 = datetime.datetime.now()
    print('Speaker said: ', final_res)
    print('Full time', t2-t1)