import discord
import asyncio
from discord.ext import commands
import os
import settings

# bot erstellen
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


# Module laden
for filename in os.listdir("./Features"):
    if filename.endswith(".py"):
        asyncio.run(bot.load_extension(f'Features.{filename[:-3]}'))


# command-message löschen
@bot.event
async def on_command(ctx):
    await asyncio.sleep(4)
    await ctx.message.delete()

# bot starten
bot.run(settings.token)
