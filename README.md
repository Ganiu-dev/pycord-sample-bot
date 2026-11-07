# ExpandoBot Sample Framework

A minimal, robust py-cord bot demonstrating a modular plugin (extension) system.

## Architecture
- `bot.py`: The main entry point. It dynamically loads all plugins from the `plugins/` directory. It includes failure isolation, meaning if one plugin has an error, the bot still starts.
- `plugins/ping.py`: A sample plugin implementing a `/ping` slash command.

## How it works
To add a feature, you drop a new file into `plugins/` with a `setup(bot)` function. `bot.py` does not need to be changed.
