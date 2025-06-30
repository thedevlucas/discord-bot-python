import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Borra una cantidad de mensajes del canal")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int = 16):
        # Limitar amount para evitar abusos (opcional)
        if amount < 1 or amount > 100:
            await interaction.response.send_message("❌ Debes borrar entre 1 y 100 mensajes.", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        try:
            await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"<a:verifed:766640990500945971> ¡Se han borrado `{amount}` mensajes!", ephemeral=False)
            await asyncio.sleep(3)
            # No podemos borrar el mensaje enviado directamente con response.send_message
            # Si quieres borrar, usa followup.send y guarda el mensaje para borrarlo después
        except Exception as e:
            await interaction.followup.send(f"Error al borrar mensajes: {e}", ephemeral=True)

    @clear.error
    async def clear_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            embed = discord.Embed(
                title="¡Mal!",
                description=f"**{interaction.user.name}** intentó borrar mensajes sin permisos.",
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/7_IWEHjEt_1GoOtDjU5lB1ndWy3vHqtPtmzgxOvhZXA/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/687630553931186276/70db4a578ad928fe488a30d3da5edb67.png?width=300&height=300")
            await interaction.followup.send(embed=embed, ephemeral=True)
            try:
                await interaction.guild.owner.send(f'{interaction.user.name} intentó borrar mensajes en el servidor {interaction.guild.name}')
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(Clear(bot))
