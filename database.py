import aiosqlite

async def warn_user(user_id , reason):
    async with aiosqlite.connect('bot.db') as db:
        await db.execute('create table if not exist warnings (user_id integer , reason Text)')

        await db.execute('insert into warnings values (?,?)' (user_id,reason))
        await db.commit()

async def get_warnings(user_id):
    async with aiosqlite.connect('bot.db') as db:
        cursor = await db.execute('select reason from warning where user_id = ?',(user_id))
        rows = await cursor.fetchall()
        return [r[0] for r in rows]

