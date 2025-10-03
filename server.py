import os
from flask import Flask
from threading import Thread
from WUQpublisher_Bot import main  # همون فایلی که کد رباتت توشه

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive ✅"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # اجرای Flask تو یه Thread جدا
    Thread(target=run_flask).start()
    # اجرای ربات
    main()
