from Answer import Answer
import os
import telebot
bot = telebot.TeleBot('6596368161:AAH_mGdLhjvWunbfenCxirkcRZp4kPssNfw')


@bot.message_handler(commands=['start', 'help'])
def send_info(message):
    bot.send_message(message.chat.id, "Отправьте аудиосообщение для распознавания эмоций")

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
        else:
            bot.send_message(message.chat.id, "Аудио не найдено...")

    except Exception as e:
        bot.send_message(message.chat.id, e)


bot.polling(none_stop=True, interval=0)
