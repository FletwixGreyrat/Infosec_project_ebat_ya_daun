import pprint
import json
import aiosqlite
from pyrogram.types import Message
from pyrogram.handlers import message_handler


from pyrogram import Client


apiId = 17384091
apiHash = "be72d42675c118dbb90c78e39b996f64"


user = Client(api_hash=apiHash, api_id=apiId, name="InfoSec")

async def getanswer(user: Client, message: Message):
    # request = message.reply_to_message.text
    # db = await aiosqlite.connect("data.db")
    # cursor = await
    # async with user:
    # print("Сообщение", message.text)
    # mssg = message
    # print("коннект")
    if message.from_user.username == "DrWebBot":
        if message.reply_to_message.document:
            zxc = message.reply_to_message.caption.split("\n")
            await user.send_message("BigInfoSec_bot", f'/send\n{zxc[0]}\n{zxc[1]}\n{message.text}')

    if message.from_user.username == "Schtirlitz_eyeofgodbot":
        msgId = message.id
        if message.reply_markup and (message.text == "Выберите доступные действия:" or message.text == "🌏 Выберите направление поиска"):
            try:
                await user.request_callback_answer(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    callback_data=message.reply_markup.inline_keyboard[0][0].callback_data,
                    timeout=20)
            except Exception:
                pass
        msg = await user.get_messages(message.chat.id, msgId)
        async for message in user.search_messages(message.chat.id):
            print(message.text)
        if message.text:
            msg = msg.text
        if message.media or message.photo or message.video:
            msg = msg.caption
    else:
        return
    db = await aiosqlite.connect("data.db")
    cursor = await db.execute("""SELECT * FROM intermediate""")
    lst = await cursor.fetchall()
    for i in lst:
        if i[1] in msg:
            await db.execute(f"INSERT INTO global (userId, answer) VALUES ('{i[0]}', '{msg}')")
            await db.commit()
            await db.execute(f"DELETE FROM intermediate WHERE request='{i[1]}'")
            await db.commit()
        # else:
        #     await db.execute(f"INSERT INTO global (userId, answer) VALUES ('{i[0]}', '🔎\n└ К сожалению, не удалось найти информации.')")
        #     await db.commit()
        #     await db.execute(f"DELETE FROM intermediate WHERE request='{i[1]}'")
        #     await db.commit()
    await db.close()




user.add_handler(message_handler.MessageHandler(getanswer))
user.run()
# client.stop()