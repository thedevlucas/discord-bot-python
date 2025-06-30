import discord
from discord import app_commands
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Muestra el avatar de un usuario.")
    @app_commands.describe(member="El miembro para mostrar el avatar. Si no se especifica, tú.")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user

        embed = discord.Embed(
            title=f"🖼️ Avatar de {member.name}",
            timestamp=discord.utils.utcnow(),
            color=discord.Color.blurple()
        )

        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed.set_image(url=avatar_url)
        embed.set_footer(text=f"Solicitado por {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Avatar(bot))
