import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Expulsa a un miembro del servidor")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member):
        if member == interaction.user:
            await interaction.response.send_message("No puedes expulsarte a ti mismo.", ephemeral=True)
            return
        try:
            await member.kick(reason=f"Kickeado por {interaction.user}")
            await interaction.response.send_message(f"**{member.name}** ha sido expulsado por **{interaction.user.name}**")
        except discord.Forbidden:
            await interaction.response.send_message("No tengo permisos para expulsar a ese usuario.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Ocurrió un error: {e}", ephemeral=True)

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            embed = discord.Embed(
                title="¡Apagando!",
                description=f"**{interaction.user.name}** intentó expulsar gente sin permisos.",
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/7_IWEHjEt_1GoOtDjU5lB1ndWy3vHqtPtmzgxOvhZXA/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/687630553931186276/70db4a578ad928fe488a30d3da5edb67.png?width=300&height=300")
            msg = await interaction.response.send_message(embed=embed, ephemeral=True)
            await asyncio.sleep(3)
            # No podemos borrar el mensaje enviado con interaction.response.send_message directamente
            # Pero si usas interaction.followup.send, podrías borrar
            try:
                await interaction.guild.owner.send(f'{interaction.user.name} intentó kickear gente en el servidor {interaction.guild.name}')
            except Exception:
                pass
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Kick(bot))
