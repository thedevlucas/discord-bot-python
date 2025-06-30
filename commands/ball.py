import random, discord
from discord import app_commands
from discord.ext import commands

class Ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ball", description="Responde aleatoriamente como una bola mágica 8.")
    async def ball(self, interaction: discord.Interaction):
        responses = [
            "Honestly, no -_- :8ball:",
            "What do you think? :8ball:",
            "I say yes, but your fate says no >u< :8ball:",
            "Don't be so sure about that. :8ball:",
            "It's likely uwu :8ball:",
            "Without a doubt! :8ball:",
            "Why the question? :8ball:",
            "Ask again later. :8ball:",
            "Don't say that... :8ball:",
            "I'm sure it'll come true. ^.^/ :8ball:",
            "No ¬¬ :8ball:",
            "Don't be so sure about that. :8ball:",
            "That's impossible. :8ball:",
            "Of course! :D :8ball:",
            "No... :8ball:",
            "That's interesting o.o :8ball:",
            "I don't think so :8ball:",
            "It's possible o.o :8ball:",
            "Yes <3 :8ball:",
            "False",
            "True",
            "Without a doubt!",
            "Supposedly, yes.",
            "Yes... :8ball:",
            "No doubt about it.",
            "Theoretically, yes :8ball:",
            "Definitely. :8ball:",
            "True :8ball:",
            "Maybe in a year >.< :8ball:",
            "Maybe in a month >.< :8ball:",
            "Maybe tomorrow >.< :8ball:",
            "Do you think so? I don’t think so ._. :8ball:",
            "Probably not. :8ball:",
            "I don't understand o.O :8ball:",
            "Of course not! >.< :8ball:"
        ]
        await interaction.response.send_message(random.choice(responses))

async def setup(bot):
    await bot.add_cog(Ball(bot))
