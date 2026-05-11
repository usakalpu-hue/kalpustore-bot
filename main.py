import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading
import json
import os

BOT_TOKEN = "7857823108:AAFneH5YiukivJuLPwRRaXOAbcyTwTQEbeA"
ADMIN_ID = 8766444295

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

DATA_FILE = "users.json"

# Create users file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Save user

def save_user(user_id, username, name):
    with open(DATA_FILE, "r") as f:
        users = json.load(f)

    exists = any(str(user["id"]) == str(user_id) for user in users)

    if not exists:
        users.append({
            "id": user_id,
            "username": username,
            "name": name
        })

        with open(DATA_FILE, "w") as f:
            json.dump(users, f, indent=4)

# Main menu

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("👤 Profile"))
    markup.add(KeyboardButton("📢 Channel"))
    markup.add(KeyboardButton("💬 Support"))
    return markup

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name

    save_user(user_id, username, name)

    bot.send_message(
        ADMIN_ID,
        f"🆕 New User Joined\n\n👤 Name: {name}\n🆔 ID: {user_id}\n📛 Username: @{username}"
    )

    bot.send_message(
        message.chat.id,
        f"🔥 Welcome {name}!",
        reply_markup=main_menu()
    )

# Buttons
@bot.message_handler(func=lambda message: True)
def buttons(message):
    text = message.text

    if text == "👤 Profile":
        bot.reply_to(
            message,
            f"👤 Name: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}"
        )

    elif text == "📢 Channel":
        bot.reply_to(message, "📢 Join Channel: https://t.me/yourchannel")

    elif text == "💬 Support":
        bot.reply_to(message, "💬 Admin: @Kalpustorexyz")

# Broadcast command
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return

    msg = message.text.replace('/broadcast ', '')

    with open(DATA_FILE, "r") as f:
        users = json.load(f)

    sent = 0

    for user in users:
        try:
            bot.send_message(user['id'], msg)
            sent += 1
        except:
            pass

    bot.reply_to(message, f"✅ Broadcast sent to {sent} users")

# Flask route
@app.route('/')
def home():
    return "Bot is running"

# Run bot

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
