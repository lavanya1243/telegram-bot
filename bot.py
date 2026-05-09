import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import os
import urllib.parse
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
    markup.add(InlineKeyboardButton("🇮🇳 India ❤️", callback_data="location_India"))
    markup.add(InlineKeyboardButton("✈️ Abroad 🌍", callback_data="location_Abroad"))
    bot.send_message(message.chat.id, "👋 Welcome! 🥰\n\nPlease select your location:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("location_"))
def location_selected(call):
    location = call.data.split("_")[1]
    user_data[call.from_user.id] = {"location": location}
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💖 Girlfriend Services 💕", callback_data="service_Girlfriend services"))
    markup.add(InlineKeyboardButton("📸 Videos & Photos 🎞️", callback_data="service_videos and photos"))
    markup.add(InlineKeyboardButton("💬 Sexting / Chatting 💋", callback_data="service_chatting")) 
    
    bot.edit_message_text(
        f"📍 Location: {location}\n\n✨ Select the service you want: ✨",
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

    # 👇 DM me aane wale message me bhi emojis lagaye gaye hain
    custom_message = f"Hi baby! ❤️ I want a service.\n📍 Location: {data['location']}\n💝 Service: {service}"
    encoded_message = urllib.parse.quote(custom_message) 
    
    contact_link = f"https://t.me/cloudhaven8?text={encoded_message}"

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "💌 Contact Me Now 💋",
            url=contact_link
        )
    )

    bot.edit_message_text(
        f"✅ Awesome Choice! 🥰\n\n"
        f"📍 {data['location']}\n"
        f"💝 {service}\n\n"
        f"👇 Click the button below to message me directly! ❤️",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

print("✅ Bot chal raha hai... ❤️✨")
bot.polling(none_stop=True)  
