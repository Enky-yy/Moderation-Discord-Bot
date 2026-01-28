 here is readme and bot stepwise creation file 
 all the directories and code mention here has been used for creating bot

 # Moderation Bot

 we have used discord.py and asyncio , itertools and sql(aiosqlite)

 discord.ext import commands,tasks
 discord import app_commands

 intents = dicord.Intents.default()
 intents.messsage_content = True
 intents.members = True

 bot=commands.bot(prefix="/", intents=intents)

## for changing status 

status= itertools.cycle([1,2,3])

@tasks.loop(seconds)
async def status():
    await bot.change_presence(
        status = discord.activity.dnd,
        type = discord.activity.type.watching,
        name= next(status)
    )


@bot.event
async def on_ready():
    print("starting....")
    await status.start()
    await bot.tree.synced()
    print('slashed command updated and active')

async load_ext():
    await bot.load_extention('dir.filename')


async start_bot(bot):
    async with bot:
        await on_ready.sart()
        bot.start('token')

asyncio run(start_bot(bot))

## ## All interaction and guild commands and functions used
