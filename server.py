# server.py
import os
import threading
from fastapi import FastAPI
import uvicorn
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------- Config ----------
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # ست کن در Render env
PORT = int(os.environ.get("PORT", 8000))
# ----------------------------

# --- Telegram handlers (نمونه: عوضش کن با هَندلِرهای خودت) ---
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ WUQ Bot is online")

# --- Function to run telegram bot (polling) in background thread ---
def run_telegram_polling():
    # بساز Application و هندلرها رو اضافه کن
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start_handler))
    # اگر هَندلرای کامل‌تری داری، اینجا add کن
    print("Starting Telegram bot (polling) ...")
    # run_polling() بلاک می‌کنه؛ پس در thread اجرا می‌کنیم
    app_bot.run_polling()

# --- FastAPI for health endpoint ---
app = FastAPI()

@app.get("/health")
async def health():
    # میتونی اطلاعات اضافی هم برگردونی مانند نسخه، uptime و ...
    return {"status": "ok"}

# Optional root page
@app.get("/")
async def root():
    return {"msg": "WUQ Bot service (web+bot) is up"}

if __name__ == "__main__":
    # start the bot in a daemon thread
    t = threading.Thread(target=run_telegram_polling, daemon=True)
    t.start()

    # start uvicorn (FastAPI) - Render will set PORT env
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, log_level="info")
