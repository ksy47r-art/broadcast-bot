import telebot
import json
import os

# --- Bot Token & Admin ID ---
BOT_TOKEN = "8202466497:AAEFxcJd57Edx8Dqf19vBLu1pKFNAqB41Vs"
ADMIN_ID = 7529704704

bot = telebot.TeleBot(BOT_TOKEN)

# --- User Database File ---
USER_DB = "users.json"

# Ensure DB file exists
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump([], f)


def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)


def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_DB, "w") as f:
            json.dump(users, f)


# --- Start Command ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    save_user(user_id)
    bot.reply_to(message, "Welcome to the bot!")


# --- Admin Broadcast Command ---
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id != ADMIN_ID:
        return bot.reply_to(message, "❌ আপনি এডমিন নন!")

    bot.reply_to(message, "✔ Broadcast পাঠাতে যে মেসেজ পাঠাতে চান সেটা রিপ্লাই করে পাঠান…")


# --- Broadcast Handler ---
@bot.message_handler(func=lambda m: m.reply_to_message and m.reply_to_message.text.startswith("✔ Broadcast"))
def send_broadcast(message):
    if message.chat.id != ADMIN_ID:
        return

    users = load_users()
    sent = 0
    failed = 0

    for user in users:
        try:
            if message.content_type == "text":
                bot.send_message(user, message.text)

            elif message.content_type == "photo":
                bot.send_photo(user, message.photo[-1].file_id, caption=message.caption)

            elif message.content_type == "video":
                bot.send_video(user, message.video.file_id, caption=message.caption)

            elif message.content_type == "sticker":
                bot.send_sticker(user, message.sticker.file_id)

            elif message.content_type == "animation":
                bot.send_animation(user, message.animation.file_id)

            sent += 1
        except:
            failed += 1

    bot.send_message(ADMIN_ID, f"📢 Broadcast Report:\n\n✔ Sent: {sent}\n❌ Failed: {failed}")


print("Bot is running…")
bot.infinity_polling()
