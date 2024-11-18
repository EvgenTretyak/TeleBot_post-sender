import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.methods import DeleteWebhook
import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=getenv('BOT_TOKEN'))

# Диспетчер
dp = Dispatcher()

# Ид чата в который будут отправлятьс голосовалки
group_id = getenv('CHAT_IT')

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Возвращает id чата
@dp.message(Command("chat_id"))
async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    await message.answer(str(chat_id))
    
# Получить текущее время сервера
@dp.message(Command("now_time"))
async def now_time(message: types.Message):
    now = datetime.datetime.now().strftime("%T-%d --> %d-%m-%Y")
    await message.answer(str(now))

@dp.message(F.text, Command("post"))
async def any_message(message: types.Message):
    await message.answer(
        "Hello, <b>world</b>!", 
        parse_mode=ParseMode.HTML
    )
    await message.answer(
        "Hello, *world*\!", 
        parse_mode=ParseMode.MARKDOWN_V2
    )

# Отправка тестового голосования в чат
@dp.message(Command("test_poll"))
async def test_poll(message: types.Message):
    await send_poll()
        

# Функция отправки голосования в чат group_id
async def send_poll():
    now = datetime.datetime.now()
    data = (now+datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    await bot.send_poll(chat_id=group_id, question=f'Идем на футбол завтра? {data}', options=['Да', 'Нет'])

# Функция отправки поста в чат group_id
async def any_message(message: Message):
    await message.answer(
        "Hello, <b>world</b>!", 
        parse_mode=ParseMode.HTML
    )
    await message.answer(
        "Hello, *world*\!", 
        parse_mode=ParseMode.MARKDOWN_V2
    )

# Планировщик отпраки голослваний
async def sheduler():
    now = datetime.datetime.now()
    while True:
        if now.weekday() == 1 and now.hour == 10:
            await send_poll
            await asyncio.sleep(60)

# Запуск процесса поллинга новых апдейтов
async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))  
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())