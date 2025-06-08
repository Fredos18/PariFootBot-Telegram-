import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from config import a620e6f2bdde6ca96235c71bb775d1ca, 8038063184:AAEWl6mg0MZ5ufuzG2tUP6nwVHIalo2vBTs, LANG

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    welcome = {
        "FR": "👋 Bienvenue sur *PariBot Football* ! Tape /matchs pour voir les prédictions.",
        "EN": "👋 Welcome to *PariBot Football*! Type /matches to see predictions."
    }
    bot.send_message(message.chat.id, welcome[LANG], parse_mode="Markdown")

@bot.message_handler(commands=['matchs', 'matches'])
def show_matches(message):
    url = "https://v3.football.api-sports.io/fixtures?date=2025-06-08&season=2024"
    headers = {"x-apisports-key": API_KEY}
    response = requests.get(url, headers=headers).json()

    matches = response.get("response", [])
    if not matches:
        bot.send_message(message.chat.id, "Aucun match trouvé." if LANG == "FR" else "No matches found.")
        return

    for match in matches[:5]:
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        time = match['fixture']['date'][11:16]
        msg = f"⚽️ {home} vs {away} à {time}"

        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("1", callback_data=f"paris:1"),
            InlineKeyboardButton("X", callback_data=f"paris:X"),
            InlineKeyboardButton("2", callback_data=f"paris:2")
        )
        markup.row(
            InlineKeyboardButton("+2.5", callback_data=f"paris:+2.5"),
            InlineKeyboardButton("-2.5", callback_data=f"paris:-2.5")
        )

        bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("paris"))
def handle_bet(call):
    choice = call.data.split(":")[1]
    reponse = {
        "FR": f"✅ Pari sélectionné : *{choice}*",
        "EN": f"✅ Selected bet: *{choice}*"
    }
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, reponse[LANG], parse_mode="Markdown")

bot.infinity_polling()
