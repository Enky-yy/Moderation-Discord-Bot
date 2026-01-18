import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!'
                   ,intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}, yehehehe')
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

