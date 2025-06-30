import discord
from discord import app_commands
from discord.ext import commands
import requests

class Bob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="bob", description="Gets text from Pastebin")
    async def bob(self, interaction: discord.Interaction):
        r = requests.get("https://pastebin.com/raw/gu2nUvMs")
        await interaction.response.send_message(r.text)

async def setup(bot):
    await bot.add_cog(Bob(bot))