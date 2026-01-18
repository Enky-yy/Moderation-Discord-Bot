import discord
from discord.ext import commands,tasks
import asyncio
import itertools

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!'
                   ,intents=intents)

statuses = itertools.cycle([
    "Watching over the server",
    "Listening to users",
    "Playing with commands"
])

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=next(statuses)
        )
    )

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}, yehehehe')
    change_status.start()
    await bot.tree.sync()
    print("Slash Command Synced")
    
async def load_ext():
    await bot.load_extension('Dept_of_mysteries.moderation')
    await bot.load_extension('Dept_of_mysteries.loggingg')
    await bot.load_extension('Dept_of_mysteries.automod')
    await bot.load_extension('Dept_of_mysteries.clear_msg')
    await bot.load_extension('Dept_of_mysteries.channels')
    await bot.load_extension('Dept_of_mysteries.temp_chnls')


secret= ''

async def main():
    async with bot:
        await load_ext()
        await bot.start(secret)

asyncio.run(main())

