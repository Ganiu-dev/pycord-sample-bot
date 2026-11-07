"""Example plugin: a /ping slash command.

Every plugin is a normal Python module that defines an async ``setup(bot)``
function. py-cord calls it at load time, and whatever the function registers on
``bot`` becomes live immediately.

To add a feature, copy this file, give it a new name, change the command — and
that is the whole process. bot.py does not need to know the file exists.
"""

from __future__ import annotations

import discord

# The plugin's message, kept as a module constant so a test or another plugin
# can assert on it without duplicating the string.
PONG_MESSAGE = "Pong! The ExpandoBot plugin system works."


def setup(bot: discord.Bot) -> None:
    """Register this plugin's commands on the bot.

    py-cord calls this once per plugin at load time. Defining commands inside
    ``setup`` keeps them local to the plugin: no module-level state leaks out,
    and the same file could in principle be loaded more than once.
    """

    @bot.slash_command(
        name="ping",
        description="Check that ExpandoBot and its plugin system are alive.",
    )
    async def ping(ctx: discord.ApplicationContext) -> None:
        # Build the reply as an embed rather than plain text. The description
        # carries the whole message, so nothing is split across fields.
        embed = discord.Embed(
            description=PONG_MESSAGE,
            colour=discord.Colour.blurple(),
        )

        # Attribution in the footer, so the reply says which plugin answered —
        # handy once there are several installed.
        embed.set_footer(text="served by the ping plugin")

        # respond() answers the interaction. It must be called exactly once per
        # interaction, within three seconds of the command being used.
        await ctx.respond(embed=embed)
