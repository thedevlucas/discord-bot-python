import discord
from discord.ext import commands
import json
import os

WELCOME_CHANNEL_ID      = 1388948330305945712
VERIFIED_ROLE_ID        = 1388948284839559311
SERVER_ID               = 1388902764762890251
UNVERIFIED_ROLE_NAME    = "unverified"

DATABASE_FOLDER = "database"
MESSAGE_ID_FILE = os.path.join(DATABASE_FOLDER, "verification_message_id.json")

def save_message_id(message_id: int):
    if not os.path.exists(DATABASE_FOLDER):
        os.makedirs(DATABASE_FOLDER)
    with open(MESSAGE_ID_FILE, "w") as f:
        json.dump({"message_id": message_id}, f)

def load_message_id():
    if not os.path.exists(MESSAGE_ID_FILE):
        return None
    with open(MESSAGE_ID_FILE, "r") as f:
        data = json.load(f)
        return data.get("message_id")

class VerificationButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.success, emoji="✅", custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        guild  = interaction.guild

        verified_role   = guild.get_role(VERIFIED_ROLE_ID)
        unverified_role = discord.utils.get(guild.roles, name=UNVERIFIED_ROLE_NAME)

        if verified_role is None:
            await interaction.response.send_message(
                "⚠️ Verified role not found. Please contact staff.", ephemeral=True
            )
            return

        try:
            await member.add_roles(verified_role, reason="User verified")
            if unverified_role in member.roles:
                await member.remove_roles(unverified_role, reason="Verification complete")

            await interaction.response.send_message(
                "You are now verified. Welcome!", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to modify your roles.", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"Unexpected error: {e}", ephemeral=True)


class VerificationMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_view(VerificationButtonView())

    @commands.Cog.listener()
    async def on_ready(self):
        if hasattr(self.bot, "_verification_message_sent"):
            return
        self.bot._verification_message_sent = True

        guild = self.bot.get_guild(SERVER_ID)
        if guild is None:
            print("⚠️ Guild not found.")
            return

        channel = guild.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            print("⚠️ Welcome channel not found.")
            return

        saved_message_id = load_message_id()

        message = None
        if saved_message_id is not None:
            try:
                message = await channel.fetch_message(saved_message_id)
                print(f"✅ Found existing verification message with ID {saved_message_id}")
            except discord.NotFound:
                print("⚠️ Saved verification message not found, will send a new one.")
            except discord.Forbidden:
                print("⚠️ Missing permissions to fetch messages in the channel.")
                return
            except Exception as e:
                print(f"⚠️ Unexpected error fetching message: {e}")
                return

        if message is None:
            embed = discord.Embed(
                title="Welcome to the server!",
                description=(
                    "Click the **Verify** button below to gain full access.\n"
                    "If you have any issues, ping a moderator."
                ),
                color=discord.Color.green(),
            )
            message = await channel.send(embed=embed, view=VerificationButtonView())
            save_message_id(message.id)
            print(f"✅ Sent new verification message and saved message ID {message.id}.")


async def setup(bot):
    await bot.add_cog(VerificationMessage(bot))
