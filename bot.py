from telegram.ext import Updater, MessageHandler, Filters
from threading import Thread
import time
import json

TOKEN = "8545215091:AAFZpTT3ixpLE8FyGFPkdtvuKKLLa1k_kF8"   # Bu yerga tokeningizni qo'ying
CHANNEL_ID = -1003208764522          # Sizning kanalingiz ID
EXPIRE_TIME = 90 * 24 * 3600         # 3 oy = 90 kun

DB_FILE = "users.json"


def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)


def new_member(update, context):
    db = load_db()
    for member in update.message.new_chat_members:
        user_id = str(member.id)
        db[user_id] = int(time.time())  # qo‘shilgan vaqtni saqlash
        save_db(db)
        print(f"{member.full_name} qo‘shildi — vaqt saqlandi.")


def checker(context):
    while True:
        db = load_db()
        now = int(time.time())

        for user_id, join_time in list(db.items()):
            if now - join_time >= EXPIRE_TIME:
                try:
                    context.bot.kick_chat_member(CHANNEL_ID, int(user_id))

                    context.bot.send_message(
                        chat_id=int(user_id),
                        text="Assalomu alaykum, sizning Joziba 18+ Premium kanalidagi obuna muddatingiz tugadi. Kanaldan foydala olmaysiz. Obunani davom ettirish uchun menedjeringizga murojaat qiling."
                    )

                    print(f"{user_id} chiqarildi va xabar yuborildi.")
                except Exception as e:
                    print("Xato:", e)

                del db[user_id]
                save_db(db)

        time.sleep(3600)  # Har 1 soatda tekshiramiz


updater = Updater(TOKEN, use_context=True)

updater.dispatcher.add_handler(
    MessageHandler(Filters.status_update.new_chat_members, new_member)
)

t = Thread(target=checker, args=(updater.bot,))
t.daemon = True
t.start()

updater.start_polling()
updater.idle()
