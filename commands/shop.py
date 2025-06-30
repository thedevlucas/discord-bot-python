import discord
from discord.ext import commands


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shop")
    async def shop(self, ctx):
        guild = ctx.guild                       # servidor actual
        title = f"{guild.name} ✅"              # título dinámico

        description = (
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📢 **All the essential links in one place!**\n"
            "From here you can access our studio website, in‑game shop and socials.\n\n"
            "🛒 **Need gems or game‑passes?** Head over to the store and power‑up your\n"
            "adventure.\n\n"
            "🌐 **Stay connected!** Follow us on social media for dev‑logs, sneak‑peeks\n"
            "and event announcements.\n\n"
            "___\n"
            "### 📜 Server Rules (Fullminate - Game Studio)\n"
            "1. Be respectful — harassment, hate speech or bullying is not tolerated.\n"
            "2. Keep all content family‑friendly (no NSFW or excessively violent media).\n"
            "3. No spamming, flooding or unsolicited advertising.\n"
            "4. Follow both **Discord TOS** and **Roblox Community Standards** at all times.\n"
            "5. Use the correct channels; keep conversations on‑topic.\n"
            "6. Do **not** leak proprietary assets, code or internal discussions.\n"
            "7. Any form of discriminatory content is prohibited.\n"
            "8. Comply with staff instructions promptly and respectfully.\n"
            "9. Report bugs or misconduct via the appropriate channels – don’t mini‑mod.\n\n"
            "Thanks for being part of our community — have fun and create awesome games together! 🛠️"
        )

        embed = discord.Embed(description=description, color=discord.Color.blurple())
        embed.title = title

        # Icono del servidor si existe
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Botones con enlaces — ajusta las URLs a las reales
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Website", emoji="🌐", url="https://your‑studio‑site.com"))
        view.add_item(discord.ui.Button(label="Shop", emoji="🛒", url="https://your‑store‑link.com"))
        view.add_item(discord.ui.Button(label="Socials", emoji="💬", url="https://linktr.ee/yourstudio"))

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Shop(bot))
