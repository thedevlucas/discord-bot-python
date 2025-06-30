import discord
from discord import app_commands
from discord.ext import commands

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unmute", description="Desmutea a un usuario")
    @app_commands.checks.has_permissions(administrator=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role is None or role not in member.roles:
            await interaction.response.send_message(f"{member.mention} no está muteado.", ephemeral=True)
            return
        
        await member.remove_roles(role, reason=f"Unmuted por {interaction.user}")

        role2 = discord.utils.get(interaction.guild.roles, name="Crying Child")
        if role2:
            await member.add_roles(role2)

        await interaction.response.send_message(f"✅ {member.mention} ha sido desmuteado.", ephemeral=False)

    @unmute.error
    async def unmute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Unmute(bot))
