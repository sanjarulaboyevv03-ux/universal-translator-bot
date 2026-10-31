import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")

user_languages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Universal Translator botiga xush kelibsiz!\n\n"
        "Tarjima tilini tanlash:\n"
        "/to en - Inglizcha\n"
        "/to ru - Ruscha\n"
        "/to uz - O‘zbekcha\n"
        "/to tj - Tojikcha\n\n"
        "Istalgan tilda matn yuboring!"
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Masalan: /to en")
        return

    lang = context.args[0].lower()
    user_languages[update.effective_user.id] = lang

    await update.message.reply_text(
        f"✅ Tarjima tili {lang} qilib belgilandi!"
    )

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang = user_languages.get(update.effective_user.id, "uz")

    try:
        result = GoogleTranslator(
            source="auto",
            target=lang
        ).translate(text)

        await update.message.reply_text("🌍 " + result)

    except Exception:
        await update.message.reply_text(
            "❌ Tarjima amalga oshmadi. Qayta urinib ko‘ring."
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("to", set_language))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, translate)
    )

    app.run_polling()

if __name__ == "__main__":
    main()
