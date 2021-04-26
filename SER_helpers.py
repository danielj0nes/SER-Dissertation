import librosa
import librosa.display
import numpy as np
from scipy.signal.signaltools import wiener
from keras.utils import np_utils
import glob

def convert_audio(path, audio_duration=3):
    """Given a path to an audio file, extract the log-scaled mel-spectrogram"""
    input_length = 44100 * audio_duration
    signal, sample_rate = librosa.load(path, sr=44100)
    signal, _ = librosa.effects.trim(signal, top_db=25)
    signal = wiener(signal)
    if len(signal) > input_length:
        signal = signal[0:input_length]
    elif input_length > len(signal):
        max_offset = input_length - len(signal)  
        signal = np.pad(signal, (0, max_offset), "constant")
    mel_spectrogram = librosa.feature.melspectrogram(signal, sr=sample_rate, n_fft=2048, hop_length=512, n_mels=128)
    lms = librosa.power_to_db(mel_spectrogram)
    lms = np.expand_dims(lms, axis=-1)
    return lms

def get_label_RAVDESS(path):
    """Given a path to a RAVDESS audio file, extract the emotion and return the label"""
    path = path.split("\\")
    gender = path[-2][6:8]
    if int(gender) % 2:
        gender = "male"
    else:
        gender = "female"
    emotion = path[-1][6:8]
    # Convert calm to neutral; surprised to happy
    emotions = {"01": "neutral", "02": "neutral",
                "03": "happy", "04": "sad",
                "05": "angry", "06": "fearful",
                "07": "disgust", "08": "happy"}
    label = gender+"_"+emotions[emotion]
    return label

labels = {0: "female_angry", 1: "female_disgust", 2: "female_fearful",
          3: "female_happy", 4: "female_neutral", 5: "female_sad",
          6: "male_angry", 7: "male_disgust", 8: "male_fearful",
          9: "male_happy", 10: "male_neutral", 11: "male_sad"}
