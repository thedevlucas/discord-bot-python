from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    async def say(self, ctx, *, arg):
        if ctx.author.guild_permissions.administrator:
            await ctx.message.delete()
            await ctx.channel.send(arg)
        else:
            await ctx.send("❌ No tienes permiso para usar este comando.")

async def setup(bot):
    await bot.add_cog(Say(bot))
