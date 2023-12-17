from textDetect import *
from emotionAUD import get_emo, emo_probs
import numpy as np
class Answer():
    def __init__(self, file_name):
        self.file = file_name
        self.message_text = recognize(file_name)
        self.text_emotion = "Не удалось распознать"
        self.audio_emotion = "Не удалось распознать"
        self.probs = {}
        self.whole_answer = "Ответ"

    def GetTextEmotion(self):
        emotion = emo_txt(self.message_text)
        emotion_dict = {'anger':'злость', 'sadness':'грусть', 'happiness':'радость', 'enthusiasm':'интерес', 'fear': 'страх', 'neutral':'нейтрально', 'disgust':'отвращение'}
        self.text_emotion = emotion_dict[emotion]

    def GetAudioEmotion(self, file_name):
        emotion_dict = {1: 'нейтральное', 3: 'радость', 4: 'грусть', 5: 'злость'}
        emotion = get_emo(file_name)
        self.audio_emotion = emotion_dict[emotion]

    def GetProbs(self, file_name):
        probs = emo_probs(file_name)
        sorted_ids = np.argsort(probs)
        emotion_dict = {1: 'нейтральное', 3: 'радость', 4: 'грусть', 5: 'злость'}
        self.probs = {}
        for el in sorted_ids:
            if el == 0:
                self.probs[emotion_dict[el + 1]] = probs[el]
            else:
                self.probs[emotion_dict[el + 2]] = probs[el]


    def create_answer(self):
        self.GetAudioEmotion(self.file)
        self.GetTextEmotion()
        #self.GetProbs(self.file)
        self.whole_answer = "*Текст сообщения:* \n" + self.message_text + "\n \n*Эмоция по голосу:* " \
                            + self.audio_emotion + "\n \n*Эмоция по тексту:* " + self.text_emotion #+ "\n\n" + str(self.probs)


