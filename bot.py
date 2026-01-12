import asyncio
import os
from aiogram import Bot, Dispatcher, types
from supabase import create_client

# Настройки (их мы вставим в облаке)
SB_URL = "ВАШ_URL_SUPABASE"
SB_KEY = "ВАШ_ANON_KEY"
BOT_TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
supabase = create_client(SB_URL, SB_KEY)

@dp.message()
async def handle_forward(message: types.Message):
    # Если переслали сообщение
    if message.forward_from or message.forward_sender_name:
        name = "Кандидат"
        if message.forward_from:
            name = message.forward_from.first_name
        elif message.forward_sender_name:
            name = message.forward_sender_name

        text = message.text or message.caption or ""
        username = ""
        if message.forward_from and message.forward_from.username:
            username = message.forward_from.username

        # Сохраняем сразу в базу Supabase
        data = {
            "recruiter_id": message.from_user.id,
            "candidate_name": name,
            "tg_username": username,
            "category": "Новые",
            "notes": [{"text": text, "date": "today"}]
        }
        
        try:
            supabase.table("candidates").insert(data).execute()
            await message.reply(f"✅ {name} добавлен в базу! Открой Mini App, чтобы увидеть его.")
        except Exception as e:
            await message.reply(f"Ошибка сохранения: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
