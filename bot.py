import discord
from discord.ext import commands

# Enable default intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# Load the plugins
bot.load_extension("plugins.ping")

if __name__ == "__main__":
    # Replace with your actual bot token if testing locally
    # bot.run("YOUR_BOT_TOKEN_HERE")
    print("Bot code is ready. Add your token to run.")
