import discord
from discord.ext import commands
import json
import os
from datetime import datetime

DATABASE_FOLDER = "database"
HISTORY_FILE = os.path.join(DATABASE_FOLDER, "history_users_list.json")

def ensure_database_folder():
    if not os.path.exists(DATABASE_FOLDER):
        os.makedirs(DATABASE_FOLDER)
        print("DEBUG: Created 'database' folder.")

def save_json(filename: str, data):
    ensure_database_folder()
    filepath = os.path.join(DATABASE_FOLDER, filename)
    print(f"DEBUG: Saving json to {filepath}")
    print(f"DEBUG: Data to be saved: {data}")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        print(f"✅ Saved data to {filepath}")
    except Exception as e:
        print(f"❌ ERROR saving json to {filepath}: {e}")

def load_json(filename: str):
    filepath = os.path.join(DATABASE_FOLDER, filename)
    if not os.path.exists(filepath):
        print(f"DEBUG: {filepath} does not exist. Creating with empty list.")
        save_json(filename, [])  # Crear archivo con lista vacía
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print(f"DEBUG: {filepath} is empty, resetting to empty list.")
                save_json(filename, [])
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"ERROR: JSON decode error in {filepath}, resetting file.")
        save_json(filename, [])
        return []
    except Exception as e:
        print(f"ERROR loading json from {filepath}: {e}")
        return []
    
def safe_attr(obj, name, default=None):
    """Devuelve obj.name si existe, si no, default."""
    return getattr(obj, name, default)

def safe_iso(dt):
    """Convierte a ISO‑8601 solo si dt no es None."""
    return dt.isoformat() if dt else None


def member_to_dict(member: discord.Member):
    def role_to_dict(role: discord.Role):
        return {
            "id": role.id,
            "name": role.name,
            "color": role.color.value,
            "position": role.position,
            "managed": role.managed,
            "mentionable": role.mentionable
        }

    def activity_to_dict(activity):
        if activity is None:
            return None
        data = {
            "type": str(activity.type),
            "name": safe_attr(activity, "name"),
            "details": safe_attr(activity, "details"),
            "state": safe_attr(activity, "state"),
            "url": safe_attr(activity, "url")
        }
        # filtra None
        return {k: v for k, v in data.items() if v is not None}

    return {
        # básicos
        "id": member.id,
        "name": member.name,
        "display_name": member.display_name,
        "discriminator": member.discriminator,
        "bot": member.bot,
        "system": safe_attr(member, "system", False),

        # avatares
        "avatar": str(member.avatar.url) if member.avatar else None,
        "default_avatar": str(member.default_avatar.url) if member.default_avatar else None,

        # fechas
        "created_at": safe_iso(safe_attr(member, "created_at")),
        "joined_at": safe_iso(safe_attr(member, "joined_at")),
        "premium_since": safe_iso(safe_attr(member, "premium_since")),
        "communication_disabled_until": safe_iso(safe_attr(member, "communication_disabled_until")),

        # otros flags
        "pending": safe_attr(member, "pending"),
        "nick": safe_attr(member, "nick"),

        # colecciones
        "roles": [role_to_dict(r) for r in member.roles],
        "activity": activity_to_dict(member.activity),
        "activities": [activity_to_dict(a) for a in safe_attr(member, "activities", [])],

        # estado
        "status": str(member.status),
        "top_role": role_to_dict(member.top_role) if member.top_role else None,
        "guild_permissions": {perm: value for perm, value in member.guild_permissions},
        "public_flags": safe_attr(member, "public_flags", []).all() if safe_attr(member, "public_flags") else None,

        # redundante pero mantengo si lo usabas
        "avatar_url": str(member.avatar.url) if member.avatar else None,
    }

class UserJoinLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        print(f"DEBUG: on_member_join fired for {member}")

        history = load_json("history_users_list.json") or []
        print(f"DEBUG: Loaded history, length={len(history)}")

        try:
            user_data = member_to_dict(member)
        except Exception as e:
            print(f"❌ ERROR: Failed to convert member to dict: {e}")
            return

        user_data["joined_timestamp"] = datetime.utcnow().isoformat()
        print(f"DEBUG: User data to append: {user_data}")

        history.append(user_data)
        print(f"DEBUG: History length after append: {len(history)}")

        save_json("history_users_list.json", history)
        print(f"✅ Saved user join info for {member}")


async def setup(bot):
    await bot.add_cog(UserJoinLogger(bot))
