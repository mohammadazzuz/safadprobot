# Bot instance setup
import os
import discord
from discord.ext import commands

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True

intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# ممكن تضيف أوامر أو أحداث تانية هون...

def run_bot():
    bot.run(BOT_TOKEN)