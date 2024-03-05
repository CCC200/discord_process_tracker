import discord
import os.path
import subprocess
from datetime import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

message_id = 0
message_channel = ""
config_array = []
is_running = False

# https://stackoverflow.com/a/29275361
def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())
#

def check_configs():
    build_string = "**SERVER STATUS:**\n"
    for data in config_array:
        exists = process_exists(data[1])
        if exists:
            build_string += ":green_circle: "
        else:
            build_string += ":red_circle: "
        build_string += data[0] + "\n"
    build_string += "\n `Updated " + str(datetime.now()) + "`"
    return build_string

async def run_cycle():
    while True:
        if not is_running:
            await asyncio.sleep(5)
            continue
        channel = client.get_channel(message_channel)
        message = await channel.fetch_message(message_id)
        build_string = check_configs()
        await message.edit(content=build_string)
        await asyncio.sleep(300)

def set_message(id, channel):
    global message_id, message_channel
    message_id = id
    message_channel = channel

def enable_cycle():
    global is_running
    is_running = True
        

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    if os.path.isfile("config.txt"):
        f = open("config.txt", "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            s = line.strip()
            a = s.split(",")
            config_array.append(a)
        print(f'Config data: {config_array}')
    else:
        raise Exception("config.txt not found")
    if os.path.isfile("tracker"):
        f = open("tracker", "r")
        s = f.read()
        a = s.split(",")
        f.close()
        set_message(int(a[0]), int(a[1]))
        print(f'Tracker message: {message_id} in {message_channel}')
        enable_cycle()
    else:
        print('Tracker not found: Use $spawn in desired channel to start bot')
    client.loop.create_task(run_cycle())
    print('Loading complete, process now looping')

@client.event
async def on_message(message):
    if message.author == client.user:
        set_message(message.id, message.channel.id)
        f = open("tracker", "w")
        f.write(str(message_id) + "," + str(message_channel))
        f.close()
        print(f'New tracker message: {message_id} in {message_channel}')
        enable_cycle()
        return

    if message.content.startswith('$spawn'):
        await message.channel.send('Setting up...')

if os.path.isfile("token.txt"):
    f = open("token.txt", "r")
    token = f.read()
    f.close()
    client.run(token)
else:
    raise Exception("token.txt not found")
