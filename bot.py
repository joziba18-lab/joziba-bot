import json
import time
import asyncio
from threading import Thread
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "8545215091:AAFZpTT3ixpLE8FyGFPkdtvuKKLLa1k_kF8"  # Tokeningiz
CHANNEL_ID = -1003208764522                                # Kanal ID
EXPIRE_TIME = 90 * 24 * 3600                               # 3 oy

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


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yangi a’zolarni DB ga yozamiz"""
    db = load_db()

    for member in update.message.new_chat_members:
        user_id = str(member.id)
        db[user_id] = int(time.time())

        save_db(db)
        print(f"{member.full_name} qo‘shildi — vaqt saqlandi.")


async def checker(app: Application):
    """Har 1 soatda muddat tugaganlarni chiqarib turadi"""
    while True:
        db = load_db()
        now = int(time.time())

        for user_id, join_time in list(db.items()):
            if now - join_time >= EXPIRE_TIME:
                try:
                    # Kanalga a’zoni chiqarish
                    await app.bot.ban_chat_member(CHANNEL_ID, int(user_id))

                    # Foydalanuvchiga xabar yuborish
                    await app.bot.send_message(
                        chat_id=int(user_id),
                        text=(
                            "Assalomu alaykum!\n"
                            "Sizning Joziba 18+ Premium kanalidagi obuna muddatingiz tugadi.\n"
                            "Davom ettirish uchun menedjeringizga murojaat qiling."
                        )
                    )

                    print(f"{user_id} chiqarildi va xabar yuborildi.")

                except Exception as e:
                    print("Xato:", e)

                del db[user_id]
                save_db(db)

        await asyncio.sleep(3600)  # 1 soat kutish


async def main():
    app = Application.builder().token(TOKEN).build()

    # Yangi a’zo handler
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))

    # Checker fon jarayoni
    Thread(target=lambda: asyncio.run(checker(app)), daemon=True).start()

    # Botni ishga tushiramiz
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
