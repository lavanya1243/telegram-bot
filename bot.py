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
    markup.add(InlineKeyboardButton("🇮🇳 India", callback_data="location_India"))
    markup.add(InlineKeyboardButton("✈️ Abroad", callback_data="location_Abroad"))
    bot.send_message(message.chat.id, "👋 Welcome!\n\nPlease select your location:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("location_"))
def location_selected(call):
    location = call.data.split("_")[1]
    user_data[call.from_user.id] = {"location": location}
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📦 Girlfriend services", callback_data="Girlfriend services"))
    markup.add(InlineKeyboardButton("📦 videos and photos", callback_data="videos and photos"))
    markup.add(InlineKeyboardButton("📦 sexting", callback_data="sexting"))
    bot.edit_message_text(
        f"📍 Location: {location}\n\nSelect your Service:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def service_selected(call):
    service = call.data.split("_", 1)[1]
    uid = call.from_user.id
    user_data[uid]["service"] = service
    data = user_data[uid]

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "📩 Contact Now",
            url="https://t.me/cloudhaven8?text=I+want+this+service"
        )
    )

    bot.edit_message_text(
        f"✅ Great Choice!\n\n"
        f"📍 {data['location']}\n"
        f"📦 {service}\n\n"
        f"👇 Click below to contact us!",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

print("✅ Bot chal raha hai...")
bot.polling(none_stop=True)
