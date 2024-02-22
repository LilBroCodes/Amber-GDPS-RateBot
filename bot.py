import json
import time
import webbrowser

import discord
import requests
from discord.ext import commands
import asyncio
import logging
import sys

from pytube import YouTube

import get_accounts
import get_levels
import get_levels as server
import get_levels_verbose
import mod_actions
import sql
from gdlib import process_levels, generate_embed, change_log_format
from colorlog import ColoredFormatter

if len(sys.argv) != 3:
    print("Usage: bot.py <channel_id> <api_key>")
    sys.exit(1)

CHANNEL_ID = int(sys.argv[1])
TOKEN = sys.argv[2]

loop = 300
loopls = [""] * 300
bot = commands.Bot(command_prefix='--', intents=discord.Intents.all())

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

formatter = ColoredFormatter(
    '[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG': 'white',
        'INFO': 'white',
        'WARNING': 'green',
        'ERROR': 'red',
        'CRITICAL': 'red',
    },
    secondary_log_colors={},
    style='%'
)


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
session = requests.Session()


async def send_level_messages(channel, processed):
    if len(processed) > 1:
        await channel.send(processed[0])
        for i, data in enumerate(processed[1:]):
            try:
                embed = generate_embed(data, processed, i)
                await channel.send(embed=embed)
            except Exception as e:
                logger.error(f"Error generating embed: {e}")
    else:
        logger.warning("Didn't find any new rated levels")


async def job():
    channel = bot.get_channel(CHANNEL_ID)

    try:
        server.save_levels_data(server.get_levels("https://amber.ps.fhgdps.com/getLevels.php", session))
        processed = process_levels("levels.json", session)
        await send_level_messages(channel, processed)
    except Exception as e:
        logger = change_log_format("main")
        logger.error(f"Error in job(): {e}")
        if "<!D" in str(e):
            with open("../error.html", "w") as error_file:
                error_file.write(str(e))


async def main_loop():
    while True:
        await job()
        shift = 300
        for _ in loopls:
            await asyncio.sleep(1)
            if shift % 10 == 0 or shift <= 3:
                print_remaining_time(shift)
            shift -= 1

def print_remaining_time(left: int):
    if left <= 60:
        logger = change_log_format("main")
        logger.info(f"Next check in {left} seconds.")
    else:
        m = str(int(left / 60))
        if len(m) == 1:
            m = f"0{m}"
        s = str(left % 60)
        if len(s) == 1:
            s = f"0{s}"
        logger = change_log_format("level_check")
        logger.info(f"Next check in {m}:{s} ({left}s)")

@bot.event
async def on_ready():
    logger = change_log_format("session")
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.loop.create_task(main_loop())


@bot.command(name="get_level", help="Sends data about a specific level from the gdps,"
                                    " input is the id of the level.")
async def get_level(ctx, level_id=93, *, debug=False):
    start_time = time.time()
    get_levels.save_levels_data(get_levels.get_levels("https://amber.ps.fhgdps.com/getLevels.php"))
    if debug:
        await ctx.send("Step 1/4, Refreshed levels.")
    with open("levels.json", "r") as file:
        levels = json.load(file)
    levels = levels.get('data')
    if debug:
        await ctx.send("Step 2/4, Imported level data")
    for level_data in levels:
        got_id = level_data["levelID"]
        if int(got_id) == level_id:
            if debug:
                await ctx.send("Step 3/4, Sending message")
            await ctx.send(embed=get_levels_verbose.gen_level_embed(level_data, debug))
            break
        else:
            continue
    if debug:
        await ctx.send(f"Step 4/4, Done in {str(time.time() - start_time)[:4]} seconds.  ")


@bot.command(name="get-acc-by-id")
async def get_accounts_id(ctx, account_id=21, *, debug=False):
    if debug:
        await ctx.send("Step 1/2, Getting accounts + generating str.")
    response = get_accounts.get_user_by_id(account_id)
    if debug:
        await ctx.send("Step 2/3, Sending message.")
    await ctx.send(response)


@bot.command(name="gdps-audit")
async def get_gdps_mod_actions(ctx, count=5):
    response = mod_actions.get_moderator_actions(count=count, url="https://amber.ps.fhgdps.com/modActions.php")
    await ctx.send(embed=response)


@bot.command(name="gdps-help", description="Lists all available commands.")
async def help_commands(ctx, command=None):
    embed = discord.Embed(
        title="Help",
        color=0x0377fc,
        description="""
            Available commands:
            --get-acc-by-id <id>
            --gdps-audit <count>
            --get-level <id>
            --help <name of command> (optional)
        """
    )
    if command is None:
        await ctx.send(embed=embed)
    else:
        if command == "get-acc-by-id":
            embed.title = f"Help for {command}"
            embed.description = ("<id> needs tp be an integer \n"
                                 " Returns the data of the account with the given id. (WIP)")
            await ctx.send(embed=embed)
        elif command == "gdps-audit":
            embed.title = f"Help for {command}"
            embed.description = ("Returns <count> mod actions from the gdps (Max is 5 for now,"
                                 " no more fit in a single message)")
            await ctx.send(embed=embed)
        elif command == "get-level":
            embed.title = f"Help for {command}"
            embed.description = ("Returns the data of the level with the given id, will later have difficulty faces, "
                                 "but it is also WIP.")
            await ctx.send(embed=embed)
        elif command == "help":
            embed.title = f"Help for {command}"
            await ctx.send(embed=embed)
        else:
            embed.description = f"No such command: {command}"
            await ctx.send(embed=embed)


@bot.command(name="sex")
async def sex(ctx):
    await ctx.send("don do dat")
    await ctx.send("https://cdn.discordapp.com/attachments/1191419321881206825/1195028652518289428/tienes_14_activa_cam_loop.mov?ex=65b28029&is=65a00b29&hm=a936eba3d3c2868a2b3316a409700309cdc61665de9ea3b7cff348fd82d54fca&")
    await ctx.send("https://cdn.discordapp.com/attachments/1191419321881206825/1191551882808791071/Screenshot_20231230_120920_TikTok.jpg?ex=65af14aa&is=659c9faa&hm=86ee8872628f73a01f1e6482209536f5b51fde8f8da3a741cb8d77d722430b58&")
    await ctx.send("https://cdn.discordapp.com/attachments/1191419321881206825/1193620322830798898/image0-2.jpg?ex=65ad608d&is=659aeb8d&hm=028d4b22a47f4fdba32db019882771ae1eb92617aa5704c4022300404070ecf2&")


def is_admin(ctx):
    return ctx.author.guild_permissions.administrator


@bot.command(name="spam")
@commands.check(is_admin)
async def spam(ctx, amount=10, message="No message provided"):
    for _ in range(amount):
        logger = change_log_format("discord_bot")
        logger.info(f"Sending message {_}/{amount}")
        await ctx.send(message)


async def play_audio(voice_channel, url):
    try:
        voice_channel.play(discord.FFmpegPCMAudio(url), after=lambda e: print('done', e, voice_channel))
    except discord.errors.ClientException as e:
        # Retry if a ClientException occurs (you can customize this based on the specific exception)
        print(f"Error during playback: {e}")
        await play_audio(voice_channel, url)


@bot.command(name='play')
async def play(ctx, *, link):
    channel = ctx.author.voice.channel

    if not channel:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    voice_channel = await channel.connect()

    try:
        # Download the YouTube video
        yt = YouTube(link)
        yt_stream = yt.streams.filter(only_audio=True).first()

        # Play the downloaded audio with retry mechanism
        await play_audio(voice_channel, yt_stream.url)

        await ctx.send(f'Now playing: {yt.title}')
    except Exception as e:
        await ctx.send(f'Error: {e}')


@bot.command(name='browser')
async def open_browser(ctx):
    # Open the default web browser
    webbrowser.open('https://www.example.com')  # You can replace this URL with the desired URL

    await ctx.send('Opening the default web browser.')


@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the bot is in a voice channel and if the voice channel is empty
    if bot.user.id == member.id and before.channel and not before.channel.members:
        await before.channel.disconnect()
        print('Bot left the voice channel.')


@bot.command(name='leave')
async def leave(ctx):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_channel:
        await voice_channel.disconnect(force=True)
        await ctx.send('Left the voice channel.')


@bot.command(name='giveto')
@commands.check(is_admin)
async def give_to(ctx, member, giveaway):
    with open("giveaways.json", "r") as file:
        giveaways = json.load(file)
    giveaways = giveaways.get('giveaways')
    if giveaway not in giveaways:
        giveaway_data = {
            "members": []
        }
        giveaways[giveaway] = giveaway_data
    giveaways.get(giveaway).get('members').append(member)
    with open("giveaways.json", "w") as file:
        giveaways = {
            "giveaways": giveaways
        }
        json.dump(giveaways, file, indent=1)
    await ctx.send(f"Successfully added {member} to the giveaway '{giveaway}'.")


@bot.command(name='list-people')
async def list_people(ctx, giveaway):
    with open("giveaways.json", "r") as file:
        giveaways = json.load(file)
    giveaways = giveaways.get('giveaways')
    if giveaway not in giveaways:
        giveaways.append(giveaway)
    members = giveaways.get(giveaway).get('members')
    embed_desc = "\n".join(members)
    embed = discord.Embed(description=embed_desc, color=int("#3d7eff"[1:], 16), title=f"Members in {giveaway}:")
    await ctx.send(embed=embed)

# Start the bot
bot.run(TOKEN)
