import telebot
import re

TOKEN = "8537712976:AAGASMWToFMzLrvMVqQa9djTJhZG4RECRSI"

bot = telebot.TeleBot(TOKEN)

warnings = {}
adds_today = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Shashlik Bot ishlayapti 🍢🔥")

@bot.message_handler(content_types=['new_chat_members'])
def count_adds(message):
    inviter_id = message.from_user.id

    if inviter_id not in adds_today:
        adds_today[inviter_id] = 0

    adds_today[inviter_id] += len(message.new_chat_members)

@bot.message_handler(commands=['top'])
def top_today(message):
    if not adds_today:
        bot.send_message(message.chat.id, "Bugun hali hech kim odam qo‘shmagan.")
        return

    text = "🔥 BUGUNGI TOP:\n\n"

    sorted_users = sorted(adds_today.items(),
                          key=lambda x: x[1],
                          reverse=True)

    for i, (user_id, count) in enumerate(sorted_users, start=1):
        user = bot.get_chat_member(message.chat.id, user_id).user
        text += f"{i}. {user.first_name} — {count} ta odam\n"

    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def anti_link(message):

    if message.chat.type == "private":
        return

    admins = bot.get_chat_administrators(message.chat.id)
    admin_ids = [admin.user.id for admin in admins]

    if message.from_user.id in admin_ids:
        return

    if message.text and re.search(r"(http|t\.me|\.com|@)", message.text):

        bot.delete_message(message.chat.id, message.message_id)

        user_id = message.from_user.id

        if user_id not in warnings:
            warnings[user_id] = 0

        warnings[user_id] += 1

        bot.send_message(message.chat.id,
                         f"⚠️ {warnings[user_id]}/3 ogohlantirish")

        if warnings[user_id] >= 3:
            bot.ban_chat_member(message.chat.id, user_id)

print("Bot ishga tushdi...")
bot.infinity_polling()
