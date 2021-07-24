import logging

from aiogram import Bot, Dispatcher, executor, types
from oxfordLookup import getDefenitions
from googletrans import Translator
translator = Translator()

API_TOKEN = 'YOUR TELEGRAM TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("ASSALOMUU ALAYKUMMM")


@dp.message_handler()
async def tarjimon(message: types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang=='en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text

        lookup = getDefenitions(word_id)
        if lookup:
            await message.reply(f"<b>Word</b>: <i>{word_id}</i> \n<b>Definitions:</b>\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.answer_voice(lookup['audio'])
        else:
            await message.reply("Bunday so'z topilmadi")    

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)