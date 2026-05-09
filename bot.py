import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============================================
# APNA TOKEN AUR USERNAME YAHAN HAI
# ============================================
TOKEN = "8725602571:AAHlPTsXviZbVGakD605tGJC9ouxRf7bAW8"
OWNER_USERNAME = "@cloudhaven8"
OWNER_ID = None  # Niche bataya hai kaise set karein
# ============================================

bot = telebot.TeleBot(TOKEN)

user_data = {}

# ============================================
# /start command
# ============================================
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🇮🇳 India", callback_data="location_India"),
        InlineKeyboardButton("✈️ Abroad", callback_data="location_Abroad")
    )
    bot.send_message(
        message.chat.id,
        "👋 Welcome!\n\nPlease select your location:",
        reply_markup=markup
    )

# ============================================
# Location select (India / Abroad)
# ============================================
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

    bot.edit_message_text(
        f"📍 Location: {location}\n\nNow select your Class/Course:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

# ============================================
# Class select
# ============================================
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

    bot.edit_message_text(
        f"📚 Course: {selected_class}\n\nNow select your Subject:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

# ============================================
# Subject select → Owner ko message
# ============================================
@bot.callback_query_handler(func=lambda call: call.data.startswith("subject_"))
def subject_selected(call):
    subject = call.data.split("_", 1)[1]
    uid = call.from_user.id
    user_data[uid]["subject"] = subject

    data = user_data[uid]

    # User ko confirmation
    bot.edit_message_text(
        f"✅ Request sent!\n\n"
        f"📍 Location: {data['location']}\n"
        f"📚 Course: {data['class']}\n"
        f"📖 Subject: {subject}\n\n"
        f"We will contact you soon! 😊",
        call.message.chat.id,
        call.message.message_id
    )

    # Owner ko message (tumhare TG pe)
    owner_message = (
        f"🔔 New Request!\n\n"
        f"👤 User: @{call.from_user.username or 'No username'}\n"
        f"🆔 User ID: {uid}\n"
        f"📍 Location: {data['location']}\n"
        f"📚 Course: {data['class']}\n"
        f"📖 Subject: {subject}\n\n"
        f"I want this service"
    )

    # Owner ka username pe message
    try:
        bot.send_message(f"@cloudhaven8", owner_message)
    except:
        pass

# ============================================
# Bot chalu karo
# ============================================
print("✅ Bot chal raha hai...")
bot.polling(none_stop=True)
