import discord
from discord import app_commands
from discord.ext import commands

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ensure_muted_role(self, guild: discord.Guild) -> discord.Role:
        role = discord.utils.get(guild.roles, name="Muted")
        if role is None:
            permissions = discord.Permissions(send_messages=False, speak=False, connect=False)
            role = await guild.create_role(name="Muted", permissions=permissions, reason="Rol para mutear usuarios creado automáticamente")
            for channel in guild.channels:
                try:
                    await channel.set_permissions(role, send_messages=False, speak=False, connect=False)
                except Exception:
                    pass
        return role

    @app_commands.command(name="mute", description="Mutea a un usuario")
    @app_commands.checks.has_permissions(administrator=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member):
        if member == interaction.user:
            await interaction.response.send_message("No te puedes mutear a ti mismo.", ephemeral=True)
            return
        
        role = await self.ensure_muted_role(interaction.guild)
        await member.add_roles(role, reason=f"Muted por {interaction.user}")
        
        role2 = discord.utils.get(interaction.guild.roles, name="Crying Child")
        if role2:
            await member.remove_roles(role2)

        await interaction.response.send_message(f"✅ {member.mention} ha sido muteado.", ephemeral=False)

    @mute.error
    async def mute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mute(bot))
