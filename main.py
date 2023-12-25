import telebot
from anime import give_rec  

bot = telebot.TeleBot("6766109465:AAGh-46FSjmV6dPyYTGJWUj14hTvSU3X528")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Введите название аниме, чтобы получить рекомендации.")

@bot.message_handler(func=lambda message: True)
def recommend_anime(message):
    user_input = message.text

    recommendations = give_rec(user_input)  

    result_message = f'Вот список похожих аниме:\n'
    for idx, anime_title in enumerate(recommendations, start=1):
        result_message += f"{idx}) {anime_title}\n"

    bot.reply_to(message, result_message)

bot.polling()