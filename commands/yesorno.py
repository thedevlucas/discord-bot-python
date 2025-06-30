import random, discord
from discord import app_commands
from discord.ext import commands

class Yn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="yesorno", description='Responde aleatoriamente "Sí" o "No".')
    async def yn(self, interaction: discord.Interaction):
        responses = [
            "Yes",
            "No",
            "Yes.",
            "No.",
            "Yes..",
            "No..."
        ]
        await interaction.response.send_message(random.choice(responses))

async def setup(bot):
    await bot.add_cog(Yn(bot))
