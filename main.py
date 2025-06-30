import discord, os
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

players = {}

@bot.command()
async def emoji(ctx, emoji: discord.Emoji):
    await ctx.send(emoji)
    print(emoji)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'¡Pong! :ping_pong: ``{latency}ms`` <a:verifed:692158056749989909>')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='/help'), status=discord.Status.do_not_disturb)
    try:
        await bot.tree.sync()
        print("✅ Global slash commands synced.")
    except Exception as e:
        print(f"⚠️ Failed to sync slash commands: {e}")
    print(f"✅ Bot is online as {bot.user}")

async def main():
    for root, dirs, files in os.walk("./commands"):
        for filename in files:
            if filename.endswith(".py"):
                relative_path = os.path.relpath(root, ".")
                module_path = relative_path.replace(os.path.sep, ".")
                extension = f"{module_path}.{filename[:-3]}"
                try:
                    await bot.load_extension(extension)
                    print(f"✅ Loaded: {extension}")
                except Exception as e:
                    print(f"❌ Failed to load {extension}: {e}")

    for filename in os.listdir("./events"):
        if filename.endswith(".py"):
            extension = f"events.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"✅ Event loaded: {extension}")
            except Exception as e:
                print(f"❌ Failed to load event {extension}: {e}")
    await bot.start('#')

asyncio.run(main())
