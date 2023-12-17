import numpy as np
import librosa
import pandas as pd



def extractor(file_path):
    # Загрузка аудиофайла
    y, sr = librosa.load(file_path, sr=None, offset=0.6)
    # Извлечение характеристик
    n_fft_val = min(1024, len(y))  # Минимум между 1024 и длиной сигнала
    hop_length_val = 256
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_fft=n_fft_val, hop_length=hop_length_val)
    rms = librosa.feature.rms(y=y)[0]
    zcr = librosa.feature.zero_crossing_rate(y=y)[0]
    chroma_n_fft = min(1024, len(y))  # Минимум между 1024 и длиной сигнала для chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=chroma_n_fft, hop_length=hop_length_val)
    tonnetz = np.mean(librosa.feature.tonnetz(chroma=chroma))

    features = [np.mean(mfcc), np.mean(rms), np.mean(zcr), np.mean(chroma), tonnetz]
    return features


import joblib
def get_emo(file_path):
    features = extractor(file_path)
    data = pd.DataFrame([features], columns=['mfcc', 'rms', 'zcr', 'chroma', 'tonnetz'])
    model = joblib.load('RandomForestModel.pkl')
    res= model.predict(data)
    return res[0]

def emo_probs(file_path):
    features = extractor(file_path)
    data = pd.DataFrame([features], columns=['mfcc', 'rms', 'zcr', 'chroma', 'tonnetz'])
    model = joblib.load('RandomForestModel.pkl')
    res = model.predict_proba(data)
    return res[0]
