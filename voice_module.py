from wav_separation.Wav_separation import Wav_separation
from vosk_api.make_print import Make_print
from vosk_api.speaker_identification import Speaker_identification


class Voice_module:
    def __init__(self):
        pass

    def separate_wav(self, path_to_stereo_wav, path_to_save_separated_wavs):
        wav_separation = Wav_separation()
        mics_signals, separated_signals, fs = wav_separation.main(path_to_stereo_wav)

        nof_speakers = len(separated_signals)
        separated_wavs = []
        for num, speaker in enumerate(range(nof_speakers), 1):
            wav_name = 'spk_' + num + '.wav'
            path_to_wav = path_to_save_separated_wavs + wav_name
            separated_wavs.append(path_to_wav)
            audio = speaker
            wav_separation.save_wav(path_to_wav, fs, audio)

        return separated_wavs

    def create_voiceprint(self, path_to_voiceprint):
        make_print = Make_print()

        print_path="./sound/Andrey/ex_1.wav"
        voice_print = make_print.create_print(path_to_voiceprint)

        return voice_print


    def main(self, path_to_stereo_wav, path_to_voiceprint, path_to_save_separated_wavs):
        speaker_identification = Speaker_identification()

        separated_wavs = self.separate_wav(path_to_stereo_wav)
        distances = []
        for sep_wav in separated_wavs:
            distance = speaker_identification.compare_with_voiceprint(sep_wav, path_to_voiceprint)
            distances.append(distance)
        
        

        print(distance)
        




if __name__ == "__main__":
    path_to_stereo_wav = './hdcam.wav'
    path_to_voiceprint = "./sound/Andrey/identification_phrase.wav"
    path_to_save_separated_wavs = 'session_1/separated_wavs/'