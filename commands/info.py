import discord
from discord.ext import commands
import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        embed = discord.Embed(
            title="Información del Usuario",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.blue()
        )
        embed.set_author(name=f"Usuario: {member}")
        embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
        embed.set_footer(text=f"Comando ejecutado por: {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Nombre para mostrar:", value=member.display_name)
        embed.add_field(name="Cuenta creada el:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Se unió el:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="¿Es un bot?", value=member.bot)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
