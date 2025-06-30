import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = 1388948330305945712
ROLE_NAME = "unverified"

class AutoUnverified(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        role = discord.utils.get(guild.roles, name=ROLE_NAME)

        if role is None:
            print(f"❌ El rol '{ROLE_NAME}' no existe en {guild.name}. No se asignará.")
            return

        try:
            await member.add_roles(role, reason="Auto‑rol unverified al unirse")
            print(f"✅ Añadido rol '{ROLE_NAME}' a {member} en {guild.name}")
        except discord.Forbidden:
            print(f"❌ No tengo permisos para asignar rol a {member}")
        except Exception as e:
            print(f"⚠️ Error al asignar rol: {e}")


async def setup(bot):
    await bot.add_cog(AutoUnverified(bot))
