from telegram import Bot
import asyncio

BOT_TOKEN = "7633955990:AAHYGIh7wu4BKTpKNz17aUgbGWnPRUFKWas"

async def main():
    bot = Bot(token=BOT_TOKEN)
    
    # حذف وب‌هوک
    result = await bot.delete_webhook()
    print("✅ Webhook deleted:", result)
    
    # بررسی وضعیت
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url:
        print("❌ هنوز وب‌هوک فعال است:", webhook_info.url)
    else:
        print("✅ وب‌هوک با موفقیت حذف شد")

# اجرا
if __name__ == "__main__":
    asyncio.run(main())
