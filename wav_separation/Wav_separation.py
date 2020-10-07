#!/usr/bin/env python

path_to_ffmpeg = '/usr/bin/ffmpeg'
import sys
sys.path.append(path_to_ffmpeg)

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import fftconvolve
import IPython
import pyroomacoustics as pra
from mir_eval.separation import bss_eval_sources
from pydub import AudioSegment
import os


class Wav_separation:
    def __init__(self):
        pass
    
    def any_exp_to_wav(self, filepath):
        (path, file_extension) = os.path.splitext(filepath)
        file_extension_final = file_extension.replace('.', '')
        filename = os.path.basename(filepath)
        dirpath = os.path.dirname(filepath)
        try:
            wav_filename = filename.replace(file_extension_final, 'wav')
            wav_path = dirpath + '/' + wav_filename
            track = AudioSegment.from_file(filepath,
                    file_extension_final)
            file_handle = track.export(wav_path, format='wav')
            os.remove(filepath)
            return wav_path
        except:
            return wav_path
        
    def create_signals_stereo(self, filepath):
        fs, signal = wavfile.read(filepath)
        signal_1 = signal[:, 0]
        signal_2 = signal[:, 1]

        signal = [signal_1, signal_2]

        return fs, signal
    
    def save_wav(self, save_path, fs, signal):
        signal = signal.astype('int16')
        wavfile.write(save_path, fs, signal)
    
    def main(self, filepath):
        fs, signals = self.create_signals_stereo(filepath)
        mics_signals = np.asarray(signals)

        L = 2048
        hop = L // 4
        win_a = pra.hamming(L)
        win_s = pra.transform.stft.compute_synthesis_window(win_a, hop)

        X = pra.transform.stft.analysis(mics_signals.T, L, hop, win=win_a)

        SDR, SIR = [], []

        def convergence_callback(Y):
            global SDR, SIR
            y = pra.transform.stft.synthesis(Y, L, hop, win=win_s)
            y = y[L - hop:, :].T


        Y = pra.bss.auxiva(X, n_iter=30, proj_back=True, callback=convergence_callback)

        y = pra.transform.stft.synthesis(Y, L, hop, win=win_s)
        y = pra.transform.stft.synthesis(Y, L, hop, win=win_s)
        y = y[L - hop:, :].T

        return mics_signals, y, fs
'''
if __name__ == "__main__":
    wav_separation = Wav_separation()
    filepath = './hdcam.wav'
    mics_signals, separated_signals, fs = wav_separation.main(filepath)
    sep_1 = separated_signals[0]
    sep_2 = separated_signals[1]
    
    wav_separation.save_wav('./spk_1.wav', fs, sep_1)
    wav_separation.save_wav('./spk_2.wav', fs, sep_2)
'''




