from flask import Flask, request
from telegram import Update
from telegram.ext import Application

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") + "/webhook"

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

if __name__ == "__main__":
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=WEBHOOK_URL
    )
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
