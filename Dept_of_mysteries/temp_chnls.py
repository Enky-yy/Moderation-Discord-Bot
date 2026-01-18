from discord.ext import commands
from discord import app_commands
import discord
import asyncio

category_id = 1462511314650927335
temp_channel_id = 1462522292855771310

from discord.ext import commands
from discord import app_commands
import discord

category_id = 1462511314650927335     # MUST be int
temp_channel_id = 1462522292855771310 # MUST be int

class TextCleanups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.text_timeout_tasks = {}

    @app_commands.command(name="temp_text")
    async def temp_text(self, interaction: discord.Interaction, name: str):
        if interaction.channel_id != temp_channel_id:
            return await interaction.response.send_message(
                "You cannot use this command here.", ephemeral=True
            )

        guild = interaction.guild
        category = guild.get_channel(category_id)   # get category object

        if category is None or category.type != discord.ChannelType.category:
            return await interaction.response.send_message(
                "Invalid category ID! Make sure it's a category.", ephemeral=True
            )

        channel = await guild.create_text_channel(name, category=category)
        await interaction.response.send_message(f"Created text channel in category: {category.name}\n{channel.mention}")

        task = asyncio.create_task(self.text_delete_timeout(channel))
        self.text_timeout_tasks[channel.id] = task

    async def text_delete_timeout(self, channel: discord.TextChannel):
        try:
            await asyncio.sleep(300)  # 5 minutes timeout
            await channel.delete()
        except asyncio.CancelledError:
            pass
        finally:
            self.text_timeout_tasks.pop(channel.id, None)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore bot messages
        if message.author.bot:
            return

        ch_id = message.channel.id

        # Reset timeout if message sent in a tracked channel
        if ch_id in self.text_timeout_tasks:
            task = self.text_timeout_tasks[ch_id]
            task.cancel()

            # restart timer
            new_task = asyncio.create_task(self.text_delete_timeout(message.channel))
            self.text_timeout_tasks[ch_id] = new_task


    


class VoiceCleanup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracked = {}

    @app_commands.command(name="temp_voice")
    async def temp_voice(self, interaction: discord.Interaction, name: str):
        if interaction.channel_id != temp_channel_id:
            return await interaction.response.send_message(
                "You cannot use this command here.", ephemeral=True
            )

        guild = interaction.guild
        category = guild.get_channel(category_id)

        if category is None or category.type != discord.ChannelType.category:
            return await interaction.response.send_message(
                "Invalid category ID!", ephemeral=True
            )

        channel = await guild.create_voice_channel(name, category=category)
        await interaction.response.send_message(f"Created voice channel in category: {category.name}\n{channel.mention}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and before.channel != after.channel:
            await self.check_cleanup(before.channel)

    async def check_cleanup(self, channel: discord.VoiceChannel):
        if not isinstance(channel, discord.VoiceChannel):
            return

        if len(channel.members) == 0:
            if channel.id not in self.tracked:
                self.tracked[channel.id] = asyncio.create_task(self.delete_after_timeout(channel))
        else:
            if channel.id in self.tracked:
                self.tracked[channel.id].cancel()
                del self.tracked[channel.id]

    async def delete_after_timeout(self, channel: discord.VoiceChannel):
        try:
            await asyncio.sleep(90)
            if len(channel.members) == 0:
                await channel.delete()
        except asyncio.CancelledError:
            pass
        finally:
            self.tracked.pop(channel.id, None)

class TempChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          # channel_id -> asyncio.Task

        # Start the inactivity timer
        


async def setup(bot):
    await bot.add_cog(TextCleanups(bot))
    await bot.add_cog(VoiceCleanup(bot))
