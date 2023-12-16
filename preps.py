import soundfile as sf

def converter(file_name):
    data, fs = sf.read(file_name)
    sf.write('audio_conv.ogg', data, fs, subtype='opus')