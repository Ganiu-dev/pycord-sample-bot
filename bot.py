"""ExpandoBot — a minimal py-cord bot with a plugin (extension) system.

Everything the bot can do lives in a plugin file under ``plugins/``. The bot
itself only knows three things: how to start, how to find its plugins, and how
to load them. Adding a feature therefore means dropping one more file into
``plugins/`` — nothing in this file changes.

Run me with:  python bot.py
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

import discord
from dotenv import load_dotenv

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

# Read DISCORD_TOKEN from a .env file next to this script, if one exists.
# The token is never hard-coded here: .env is git-ignored.
load_dotenv(Path(__file__).with_name(".env"))

# The folder holding the plugins. Resolved from this file's own location, so
# the bot works no matter which directory you launch it from.
PLUGINS_DIR = Path(__file__).with_name("plugins")

# DEBUG=1 in the environment gives verbose library logging.
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(name)s: %(message)s",
)
log = logging.getLogger("expandobot")


# --------------------------------------------------------------------------
# The bot
# --------------------------------------------------------------------------

class ExpandoBot(discord.Bot):
    """The bot object, with plugin loading built in.

    Subclassing ``discord.Bot`` rather than using it directly is not strictly
    required, but it gives plugin loading a natural home and lets a plugin
    reach the bot through ``ctx.bot`` if it needs to.
    """

    async def setup_hook(self) -> None:
        """Called by py-cord once, just before the gateway connects.

        This is the right place to load plugins: the bot is running its event
        loop by now, but no command has been dispatched yet, so nothing can
        arrive before its handler exists.
        """
        self.load_plugins()

    def load_plugins(self) -> None:
        """Load every ``*.py`` file in ``plugins/`` as an extension.

        A file only counts as a plugin if it defines ``setup(bot)`` — py-cord
        calls that function and expects it to register the commands. A file
        without it, or one that raises on import, is logged and skipped: one
        broken plugin must not stop the bot from starting.
        """
        if not PLUGINS_DIR.is_dir():
            log.warning("no plugins directory at %s", PLUGINS_DIR)
            return

        # Extensions are imported as the package "plugins.ping", so the folder
        # containing "plugins/" has to be importable. Running "python bot.py"
        # puts it on sys.path already; adding it explicitly means the bot also
        # loads its plugins when launched from elsewhere, e.g.
        # "python /srv/expando-bot/bot.py" from a cron job.
        base = str(PLUGINS_DIR.parent)
        if base not in sys.path:
            sys.path.insert(0, base)

        found = 0
        for path in sorted(PLUGINS_DIR.glob("*.py")):
            # Ignore __init__.py and any private helper modules such as
            # plugins/_helpers.py: only names without a leading underscore are
            # treated as plugins.
            if path.name.startswith("_"):
                continue

            # py-cord loads extensions by dotted module path, so "plugins/ping.py"
            # becomes "plugins.ping". The folder itself needs no __init__.py.
            module = f"{PLUGINS_DIR.name}.{path.stem}"
            try:
                self.load_extension(module)
            except Exception:
                # Log the whole traceback and carry on with the next plugin.
                log.exception("plugin %r failed to load", module)
            else:
                found += 1
                log.info("loaded plugin %r", module)

        log.info("%d plugin(s) loaded", found)


def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit(
            "DISCORD_TOKEN is not set. Copy .env.example to .env and paste your "
            "bot token in, or export DISCORD_TOKEN in your shell."
        )

    # No privileged intents are needed: this bot reacts to slash commands,
    # which Discord delivers without the message-content intent.
    bot = ExpandoBot()
    bot.run(token)


if __name__ == "__main__":
    main()
