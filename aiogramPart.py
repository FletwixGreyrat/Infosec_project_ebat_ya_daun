import json
import pprint
import asyncio
import aiogram
import aiosqlite
from FSM import coderFSM, OSINTFSM, antivirusFSM
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from keyboards import startKb, otmenaAntivirus, otmenaKrypto, otmenaOsint, codeOrDecode

storage = MemoryStorage()
bot: Bot = Bot(token="6968925615:AAFJgDjfBiSAvP6165v0bZdXbvXqHpbawfg")
dp: Dispatcher = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def startCmd(message: types.Message):
    await message.answer('Привет!!! Я, Big InfoSec бот, помогу тебе в контексте кибербезопасности', reply_markup=startKb())

@dp.message_handler(lambda message: message.text == "OSINT🖥️", state=None)
async def getOsint(message: types.Message, state: FSMContext):
    await message.answer("Введите ваш запрос:", reply_markup=otmenaOsint())
    await OSINTFSM.request.set()


@dp.message_handler(content_types=['text', 'photo', 'video', "sticker"], state=OSINTFSM)
async def getOSINTRequest(message: types.Message, state: FSMContext):
    print(123)
    dct = dict()
    async with state.proxy() as data:
        data["request"] = message.text if message.text else message.caption
        data["id"] = message.from_user.id  
        dct = data
    from someFunctions import osint
    await state.finish()
    await osint(dct["request"], dct["id"])
    print(123)
    count = 0
    flag = False
    while count <= 60:
        print("zxc")
        db = await aiosqlite.connect("data.db")
        cursor = await db.execute(f"SELECT * FROM global WHERE userId={message.from_user.id}")
        lst = await cursor.fetchall()
        await cursor.close()
        if len(lst) == 0:
            count += 1
            await asyncio.sleep(1)
            continue
        else:
            await message.answer(lst[-1][1])
            await db.execute(f'DELETE FROM global WHERE userId="{message.from_user.id}"')
            await db.commit()
            flag = True
        await db.commit()
        await db.close()
        print(123)
        await asyncio.sleep(1)
        count += 1
    
    if not flag:
        await message.answer("К сожалению, не удалось найти информации по вашему запросу")    

        
        


@dp.message_handler(lambda message: message.text == "Антивирус🦠", state=None)
async def getAntivirusRequest(message: types.Message, state: FSMContext):
    await message.answer("Отправь мне файл на проверку:", reply_markup=otmenaAntivirus())
    await antivirusFSM.request.set()

@dp.message_handler(content_types=["any"], state=antivirusFSM)
async def downloadDocument(message: types.Message, state: FSMContext):
    if not (message.document):
        await message.answer("Ошибка! Аргумент для проверки должен быть отправлен как файл, попробуйте еще раз", reply_markup=otmenaAntivirus())
    if message.document:
        from someFunctions import antivirus
        info = await bot.get_file(message.document.file_id)
        await message.document.download()
        print("zxc")
        await antivirus(info.file_path, message.message_id, message.from_user.id)
        print(123)
        await state.finish()


@dp.message_handler(lambda message: message.text == "Шифровщик/дешифровщик📄")
async def getCoderRequest(message: types.Message):
    await message.answer("Выберите опцию", reply_markup=codeOrDecode())

@dp.callback_query_handler(text_startswith="code:", state=None)
async def coding(call: types.CallbackQuery, state: FSMContext):
    if call.data.split(":")[1] == "coding":
        await coderFSM.request.set()
        async with state.proxy() as data:
            data["state"] = "coding"
        await call.message.answer("Отправьте файл на шифрование:", reply_markup=otmenaKrypto())
    elif call.data.split(":")[1] == "decode":
        await coderFSM.request.set()
        async with state.proxy() as data:
            data["state"] = "decode"
        await call.message.answer("Отправьте зашифрованный код:", reply_markup=otmenaKrypto())
    return


@dp.message_handler(commands=["send"])
async def sendAntivirusAnswer(message: types.Message):
    msg = message.text.split("\n")
    await bot.send_message(reply_to_message_id=msg[1], chat_id=msg[2], text=msg[3])

@dp.message_handler(content_types=["any"], state=coderFSM)
async def codingHandling(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        dat = data["state"]
    if dat == "coding":
        if message.text:
            await message.answer("Ошибка типа данных. Отправить можно что угодно, кроме текста. Если вам так сильно хочется, можете отправить текстовый файл, я зашифрую его)))", reply_markup=otmenaKrypto())
            return
        async with state.proxy() as data:
            if message.photo:
                data["type"] = "photo"
                data["id"] = message.photo[0].file_id
            if message.video:
                data["type"] = "video"
                data["id"] = message.video.file_id
            if message.voice:
                data["type"] = "voice"
                data["id"] = message.voice.file_id
            if message.video_note:
                data["type"] = "video_note"
                data["id"] = message.video_note.file_id
            if message.document:
                data["type"] = "document"
                data["id"] = message.document.file_id
            if message.audio:
                data["type"] = "audio"
                data["id"] = message.audio.file_id

            db = await aiosqlite.connect("data.db")
            await db.execute(f"""INSERT INTO cloud (fileId, dataType) VALUES ('{data["id"]}', '{data['type']}')""")
            idshka = data['id']
            await message.answer(f"Готово! Вот ваш зашифрованный файл:\n\n<code>{idshka}</code>", parse_mode=types.ParseMode.HTML)
            await db.commit()
            await db.close()
            await state.finish()
    else:
        if not (message.text):
            await message.answer("Ошибка типа данных. Для дешифровки нужно предоставить тексовое сообщение с шифром", reply_markup=otmenaKrypto())
            return
        fileId = message.text
        db = await aiosqlite.connect("data.db")
        cursor = await db.execute(f"""SELECT * FROM cloud WHERE fileId='{fileId}'""")
        lst = await cursor.fetchone()
        print(lst)
        if lst is None:
            await message.answer("Ошибка! Данный шифр не несет за собой никакого файла, попробуйте еще раз", reply_markup=otmenaKrypto())
            return
        if lst[1] == "photo":
            await bot.send_photo(message.from_user.id, photo=lst[0])
        if lst[1] == "video":
            await bot.send_video(message.from_user.id, video=lst[0])
        if lst[1] == "voice":
            await bot.send_voice(message.from_user.id, voice=lst[0])
        if lst[1] == "video_note":
            await bot.send_video_note(message.from_user.id, video_note=lst[0])
        if lst[1] == "document":
            await bot.send_document(message.from_user.id, document=lst[0])
        if lst[1] == "audio":
            await bot.send_audio(message.from_user.id, audio=lst[0])
        await state.finish()
        return
    
        
    


    
@dp.callback_query_handler(text="break", state=OSINTFSM)
async def osintBreakCallback(call: types.CallbackQuery, state: FSMContext):
    print(123)
    await state.finish()
    await call.message.answer("Поиск отменен")


@dp.callback_query_handler(text="break", state=antivirusFSM)
async def osintBreakCallback(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Проверка отменена")


@dp.callback_query_handler(text="break", state=coderFSM)
async def osintBreakCallback(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Действие отменено...")



if __name__ == "__main__":
    aiogram.executor.start_polling(dispatcher=dp, skip_updates=True)
