from Answer import Answer
import os
import telebot
from telebot import types
bot = telebot.TeleBot('6596368161:AAH_mGdLhjvWunbfenCxirkcRZp4kPssNfw')


@bot.message_handler(commands=['start', 'help'])
def send_info(message):
    user = message.from_user
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/start")
    btn2 = types.KeyboardButton("/help")
    markup.add(btn1, btn2)
    if message.text == "/start":
        bot.send_message(message.chat.id, f"Здравствуйте, {user.first_name}. Отправьте аудиосообщение продолжительностью до 30 секунд для распознавания эмоций",
                     reply_markup=markup)
    if message.text == "/help":
        bot.send_message(message.chat.id,
                     "Этот бот распознает текст, эмоции по голосу и по содержанию коротких голосовых сообщений. "
                     "\n Запишите своё аудиосообщение или перешлите боту сообщение от Вашего собеседника.",
                     reply_markup=markup)

@bot.message_handler(content_types=['text', 'photo', 'video', 'video_note'])
def send_info(message):
    bot.send_message(message.chat.id, "Бот пока умеет распознавать только аудио \n:(")

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    try:
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)

        file = bot.download_file(file_info.file_path)

        with open('audio.wav', 'wb') as new_file:
            new_file.write(file)
        if os.path.exists('audio.wav'):
            bot.send_message(message.chat.id, "Аудио получено, обрабатывается...")
            answer = Answer('audio.wav')
            answer.create_answer()
            bot.send_message(message.chat.id, answer.whole_answer, parse_mode='Markdown')
            os.remove('audio.wav')
        else:
            bot.send_message(message.chat.id, "Аудио не найдено...")

    except Exception as e:
        bot.send_message(message.chat.id, e)


bot.polling(none_stop=True, interval=0)
