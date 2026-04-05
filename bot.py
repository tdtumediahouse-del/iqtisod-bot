import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse

# ==========================================
# 1. BOT VA SAYT SOZLAMALARI
# ==========================================
TOKEN = '8702951795:AAFD1rpDI1SYOIXfZ_z1JSBp-_FjrG4tB9c'
WEB_APP_URL = 'https://iqtisodchilar.uz'

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# ==========================================
# 2. MUKAMMAL MENYU VA FUNKSIYALAR
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(text="📝 Imtihonni boshlash", web_app=WebAppInfo(url=WEB_APP_URL)))
    markup.add(KeyboardButton(text="🚀 Kabinetga kirish", web_app=WebAppInfo(url=WEB_APP_URL)))
    markup.add(KeyboardButton("🧮 Aqlli Kalkulyator"), KeyboardButton("👨‍💻 Aloqa Markazi"))
    markup.add(KeyboardButton("💎 Platforma haqida"))
    
    welcome_text = (
        f"<b>Assalomu alaykum, {message.from_user.first_name}! ✨</b>\n\n"
        "<b>TDTU Iqtisodchilar</b> — raqamli iqtisodiyot va menejment platformasiga xush kelibsiz.\n\n"
        "Mavjud imkoniyatlar:\n"
        "🎓 <b>Imtihonlar:</b> Bilimingizni real vaqtda sinang\n"
        "📊 <b>Dashboard:</b> Shaxsiy natijalar va reytinglar\n"
        "🧮 <b>Kalkulyator:</b> Murakkab iqtisodiy formulalar\n\n"
        "<i>Iltimos, ishlashni boshlash uchun kerakli bo'limni tanlang:</i>"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🧮 Aqlli Kalkulyator")
def eco_calculator(message):
    text = (
        "<b>🧮 Aqlli Iqtisodiy Kalkulyator</b>\n\n"
        "Makro va mikro iqtisodiyotga oid barcha formulalar bitta joyda jamlangan. "
        "YaIM, inflyatsiya, talab elastikligi va boshqa ko'rsatkichlarni soniyalar ichida hisoblang."
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🌐 Kalkulyatorni ishga tushirish", web_app=WebAppInfo(url=WEB_APP_URL)))
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "👨‍💻 Aloqa Markazi")
def contact_admin(message):
    # AVTOMATIK SHABLON (Foydalanuvchi ism-familiyasini Telegramdan tortib olamiz)
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    
    template = (
        "Assalomu alaykum! Men platforma yuzasidan murojaat qilyapman.\n\n"
        f"👤 Ism: {first_name}\n"
        f"👥 Familiya: {last_name}\n"
        "📞 Bog'lanish uchun raqam: \n"
        "📝 Muammo yoki taklif: "
    )
    
    # Matnni URL formatiga o'tkazish
    url_template = urllib.parse.quote(template)
    admin_link = f"https://t.me/mirsoat_xolmurodov?text={url_template}"
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("📨 Adminga xabar yozish", url=admin_link))
    
    contact_text = (
        "<b>🎧 24/7 Aloqa Markazi</b>\n\n"
        "Platforma ishlashida xatolik topdingizmi yoki ajoyib taklifingiz bormi? "
        "Biz sizni tinglashga doim tayyormiz!\n\n"
        "💡 <b>Qulaylik:</b> Tizim ism va familiyangizni <b>avtomatik tarzda shablonga joyladi</b>. "
        "Pastdagi tugmani bosing, faqat telefon raqamingiz va muammoni yozib yuboring."
    )
    bot.send_message(message.chat.id, contact_text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💎 Platforma haqida")
def about_bot(message):
    text = (
        "<b>🏛 TDTU Iqtisodchilar — Zamonaviy Talaba Ekosistemasi</b>\n\n"
        "Bu loyiha Toshkent Davlat Texnika Universiteti talabalarining analitik va iqtisodiy bilimlarini "
        "raqamlashtirish maqsadida yaratilgan eksklyuziv platformadir.\n\n"
        "👨‍💻 <b>Asoschi va Dasturchi:</b> Mirsoat Xolmurodov\n"
        "🛡 <b>Xavfsizlik:</b> End-to-End himoyalangan\n"
        "🚀 <b>Server:</b> High-Performance Render\n"
        "💡 <b>Versiya:</b> 7.0 (Premium Tizim)"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# ==========================================
# 3. UXLAMAYDIGAN SERVER QISMI (WEBHOOK)
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
    return "🚀 TDTU Iqtisodchilar platformasi 24/7 ishlamoqda!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000)))
