import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)
user_data = {}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass

def run_server():
    HTTPServer(("0.0.0.0", 10000), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🇮🇳 India", callback_data="location_India"),
        InlineKeyboardButton("✈️ Abroad", callback_data="location_Abroad")
    )
    bot.send_message(message.chat.id, "👋 Welcome!\n\nPlease select your location:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("location_"))
def location_selected(call):
    location = call.data.split("_")[1]
    user_data[call.from_user.id] = {"location": location}
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📘 Class 11", callback_data="class_Class 11"),
        InlineKeyboardButton("📗 Class 12", callback_data="class_Class 12")
    )
    markup.add(
        InlineKeyboardButton("🧪 NEET", callback_data="class_NEET"),
        InlineKeyboardButton("📐 JEE", callback_data="class_JEE")
    )
    bot.edit_message_text(f"📍 Location: {location}\n\nSelect your Class/Course:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("class_"))
def class_selected(call):
    selected_class = call.data.split("_", 1)[1]
    user_data[call.from_user.id]["class"] = selected_class
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("⚡ Physics", callback_data="subject_Physics"),
        InlineKeyboardButton("🧪 Chemistry", callback_data="subject_Chemistry")
    )
    markup.add(
        InlineKeyboardButton("📐 Maths", callback_data="subject_Maths"),
        InlineKeyboardButton("🌿 Biology", callback_data="subject_Biology")
    )
    bot.edit_message_text(f"📚 Course: {selected_class}\n\nSelect your Subject:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("subject_"))
def subject_selected(call):
    subject = call.data.split("_", 1)[1]
    uid = call.from_user.id
    user_data[uid]["subject"] = subject
    data = user_data[uid]
    bot.edit_message_text(
        f"✅ Request sent!\n\n📍 {data['location']}\n📚 {data['class']}\n📖 {subject}\n\nWe will contact you soon! 😊",
        call.message.chat.id, call.message.message_id
    )
    try:
        bot.send_message("@cloudhaven8",
            f"🔔 New Request!\n👤 @{call.from_user.username or 'No username'}\n📍 {data['location']}\n📚 {data['class']}\n📖 {subject}\n\nI want this service"
        )
    except:
        pass

print("✅ Bot chal raha hai...")
bot.polling(none_stop=True)
