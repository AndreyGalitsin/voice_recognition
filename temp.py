from wav_separation.Wav_separation import Wav_separation


if __name__ == "__main__":
    wav_separation = Wav_separation()

    filepaths = ['./vosk_api/sound/Andrey/ex_3.m4a', './vosk_api/sound/Katya/ex_1.m4a']
    for file in filepaths:
        wav_separation.m4a_to_wav(file)