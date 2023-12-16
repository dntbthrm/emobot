import os
import urllib.request
import json
from preps import  *
def recognize(audio_wav):
    IAM_TOKEN = "t1.9euelZqPzJackM3MiYyJiZXOz4qaie3rnpWajZPIxp3GmZSKnZSMjJXGmJfl8_dMVwhU-e9FFEQK_t3z9wwGBlT570UURAr-zef1656VmsuQj5GczJaOmc2MmZadkMyQ7_zF656VmsuQj5GczJaOmc2MmZadkMyQ.ojPxt6QX4gvO2CsBA4qsaj1hE_MCqdXvLjtRSds4bBXgW1vvPbzoXgTFEoqsIb2Qn46Ze_fXd57-mfnZDvYXDQ"
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
    # Аутентификация через IAM-токен.
    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)
    text = "hoho"
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