# Discord Process Tracker

A simple tool that does the following:
- Tracks whether a list of predefined processes are running on the local machine
- Displays each process status via Discord bot

## Instructions

Before starting, ensure you have a working python3 installation and [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html#installing) is installed. You are also expected to setup and configure your own Discord bot as that is not in the scope of these instructions.

1. Create `token.txt` in this directory and paste your bot token
2. Make a copy of `config_example.txt` and rename it to `config.txt`
3. Add your processes following the `name,processname` format in the example file
4. Run `discord_process_tracker.py`
5. Go to your desired channel and enter `$spawn` to start the bot
