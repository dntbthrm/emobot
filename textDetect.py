import os
import urllib.request
import json
from preps import  *
def recognize(audio_wav):
    # данные для аутентификации
    IAM_TOKEN = "t1.9euelZrKlsiWj5Wck86LnM3JmZGLzO3rnpWajZPIxp3GmZSKnZSMjJXGmJfl9PdPaARU-e8kfhvp3fT3DxcCVPnvJH4b6c3n9euelZqNmY3IzZnJyJyZjseSjsvKzO_8xeuelZqNmY3IzZnJyJyZjseSjsvKzA.enlM81uuXokzc8lgwpMsq0CVSlG6MklU-fYTwpa9ZkiiX3f2LNEQ4DqC38vt_TjekaUJuop7RqJVXeGUFC8EDw"
    FOLDER_ID = "b1gf4gqnn6p5j7irohgr"
    converter(audio_wav)
    with open("audio_conv.ogg", "rb") as f:
        data = f.read()

    params = "&".join([
        "topic=general",
        "folderId=%s" % FOLDER_ID,
        "lang=ru-RU",
        "sampleRateHertz=48000"
    ])

    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
    # аутентификация
    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)
    text = "Текст не распознан"
    if decodedData.get("error_code") is None:
        text = decodedData.get("result")
    os.remove('audio_conv.ogg')
    return text



import torch
from aniemore.recognizers.text import TextRecognizer
from aniemore.models import HuggingFaceModel
def emo_txt(text_got):
    model = HuggingFaceModel.Text.Bert_Tiny2
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tr = TextRecognizer(model=model, device=device)
    return tr.recognize(text_got, return_single_label=True)