# -*- coding: utf-8 -*-
import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler,
    ContextTypes, filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

TITLE, PURCHASABLE, TYPE, STOCK = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎨 لطفاً عنوان/تیتر پست رو بفرست:")
    return TITLE

async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text
    await update.message.reply_text("آیا طرح قابل خرید است؟\n1 = #purchasable\n2 = #unpurchasable")
    return PURCHASABLE

async def get_purchasable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip()
    if choice == "1":
        context.user_data["purchasable"] = True
        await update.message.reply_text("نوع طرح را مشخص کن:\n1 = Standard\n2 = WUQ Limited")
        return TYPE
    elif choice == "2":
        context.user_data["purchasable"] = False
        await send_caption(update, context)
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ فقط 1 یا 2 بفرست.")
        return PURCHASABLE

async def get_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip()
    if choice == "1":
        context.user_data["type"] = "Standard"
        await send_caption(update, context)
        return ConversationHandler.END
    elif choice == "2":
        context.user_data["type"] = "WUQ Limited"
        await update.message.reply_text("🔢 تعداد کل استاک رو وارد کن (مثلاً: 5)")
        return STOCK
    else:
        await update.message.reply_text("❌ فقط 1 یا 2 بفرست.")
        return TYPE

async def get_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stock = update.message.text.strip()
    if not stock.isdigit():
        await update.message.reply_text("❌ لطفاً عدد بفرست.")
        return STOCK
    context.user_data["stock"] = int(stock)
    await send_caption(update, context)
    return ConversationHandler.END

async def send_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = context.user_data.get("title", "🎨 #Design")
    purchasable = context.user_data.get("purchasable", False)
    design_type = context.user_data.get("type", None)
    stock = context.user_data.get("stock", None)

    caption = f"{title}\n\n"

    if purchasable:
        caption += "🛒 : #purchasable\n"
        caption += "📦 Status: 🟢 Available\n"
        if design_type == "Standard":
            caption += "🔑 Type: 🟠 Standard\n"
        elif design_type == "WUQ Limited":
            caption += "🔑 Type: 🟡 WUQ Limited\n"
            caption += f"#️⃣ Stock Left: {stock}/{stock}\n"
    else:
        caption += "🛒 : #unpurchasable\n"

    caption += "\n📛 Channel ID: @WUQStudio"

    await update.message.reply_text(caption)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ عملیات لغو شد.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
            PURCHASABLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_purchasable)],
            TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_type)],
            STOCK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_stock)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("🤖 Bot is running...")

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
