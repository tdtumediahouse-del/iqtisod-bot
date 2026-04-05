import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse

# BOT SOZLAMALARI
TOKEN = '8702951795:AAFD1rpDI1SYOIXfZ_z1JSBp-_FjrG4tB9c'
WEB_APP_URL = 'https://iqtisodchilar.uz'

bot = telebot.TeleBot(TOKEN, threaded=False)
(threaded=False
app = Flask(__name__)

# ==========================================
# SIZNING BOT FUNKSIYALARINGIZ
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(text="📝 Imtihonni boshlash", web_app=WebAppInfo(url=WEB_APP_URL)))
    markup.add(KeyboardButton(text="🚀 Kabinetga kirish", web_app=WebAppInfo(url=WEB_APP_URL)))
    markup.add(KeyboardButton("🧮 Aqlli Kalkulyator"), KeyboardButton("👨‍💻 Bog'lanish"))
    markup.add(KeyboardButton("💎 Bot haqida"))
    
    bot.send_message(message.chat.id, f"<b>Assalomu alaykum, {message.from_user.first_name}! ✨</b>\n\n<b>TDTU Iqtisodchilar</b> platformasining rasmiy botiga xush kelibsiz.", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🧮 Aqlli Kalkulyator")
def eco_calculator(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🌐 Kalkulyatorni ochish", web_app=WebAppInfo(url=WEB_APP_URL)))
    bot.send_message(message.chat.id, "<b>🧮 Aqlli Iqtisodiy Kalkulyator</b>\nBarcha formulalar web-ilovada.", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "👨‍💻 Bog'lanish")
def contact_admin(message):
    template = urllib.parse.quote("Guruh: \nMuammo: ")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📩 Telegram orqali yozish", url=f"https://t.me/mirsoat_xolmurodov?text={template}"))
    bot.send_message(message.chat.id, "<b>💎 Professional Aloqa Markazi</b>", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💎 Bot haqida")
def about_bot(message):
    bot.send_message(message.chat.id, "<b>🏛 TDTU Iqtisodchilar Platformasi</b>\n🚀 <b>Versiya:</b> 6.0 (Render Server - 24/7)", parse_mode="HTML")

# ==========================================
# ==========================================
# SERVER VA WEBHOOK (UXLAMAYDIGAN YURAK)
# ==========================================
@app.route('/' + TOKEN, methods=['POST'])
def receive_update():
    try:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        print("XATOLIK:", e)
        return "Error", 500

@app.route('/')
def index():
    return "🚀 TDTU Iqtisodchilar Boti Render.com serverida 24/7 ishlamoqda!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000)))
