import aiosqlite
from pyrogram import Client


apiId = 17384091
apiHash = "be72d42675c118dbb90c78e39b996f64"


client = Client(api_hash=apiHash, api_id=apiId, name="sender")


async def osint(request, userId):
    async with client:
        db = await aiosqlite.connect("data.db")
        await client.send_message("Schtirlitz_eyeofgodbot", request)
        await db.execute(f"""INSERT INTO intermediate (userId, request) VALUES ('{userId}', '{request}')""")
        await db.commit()
        await db.close()

async def antivirus(path, messageId, userId):
    async with client:
        db = await aiosqlite.connect("data.db")
        doc = open(path, "rb")
        print("zxczxc")
        await client.send_document("DrWebBot", document=doc, caption=f"{messageId}\n{userId}")
        print(456)


# client.start()
# client.send_message("Schtirlitz_eyeofgodbot", 'zxczxczxcz')
# client.stop()