import json
import logging
import os.path

import discord
import time
import requests
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler
from datetime import datetime

current_time = datetime.now()
time_string = current_time.strftime("%Y-%m-%d_%H")

if not os.path.isdir("logs/"):
    os.makedirs("logs")

file_handler = RotatingFileHandler(f"logs/{time_string}.log", maxBytes=10 * 1024 * 1024, backupCount=5)


def change_log_format(name: str):
    new_logger = logging.getLogger(name)
    new_logger.setLevel(logging.INFO)

    new_formatter = ColoredFormatter(
        f'[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s',
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
    new_logger.addHandler(file_handler)

    new_stream_handler = logging.StreamHandler()
    new_stream_handler.setFormatter(new_formatter)
    new_logger.addHandler(new_stream_handler)
    return new_logger


def get_gd_diff(diff: int, auto: int, demon: int):
    if auto != 0:
        return "Auto"
    elif demon != 0:
        return "Demon"
    else:
        if diff == 0:
            return "N/A"
        elif diff == 10:
            return "Easy"
        elif diff == 20:
            return "Normal"
        elif diff == 30:
            return "Hard"
        elif diff == 40:
            return "Harder"
        elif diff == 50:
            return "Insane"
        else:
            return "Unknown"


def process_levels(filename, session: requests.Session):
    with open(filename, "r") as file:
        levels = json.load(file)
    levels = levels.get('data')

    extracted = []
    for level in levels:
        extract = ["userName", "levelID", "levelName", "starDifficulty", "levelDesc",
                   "likes", "downloads", "starStars", "starDemon", "starAuto"]
        out = {key: level[key] for key in extract}
        extracted.append(out)

    return_message = f"<@&{1190047680743878707}> New rated level!"
    return_levels = [return_message]
    try:
        for level_data in extracted:
            with open("processed", "r") as opened:
                processed = opened.read()
            level_name = str(level_data["levelName"])
            if level_name not in processed and int(level_data["starStars"]) > 0:
                difficulty_stars = int(level_data["starDifficulty"])
                auto = int(level_data["starAuto"])
                demon = int(level_data["starDemon"])
                author = level_data["userName"]
                level_id = level_data["levelID"]
                difficulty_text = f"{get_gd_diff(difficulty_stars, auto, demon)}, {level_data['starStars']}"
                if int(level_data["starStars"]) == 1:
                    difficulty_text = f"{difficulty_text} star"
                else:
                    difficulty_text = f"{difficulty_text} stars"
                return_level_data = {
                    "level_name": level_name,
                    "author": author,
                    "difficulty": difficulty_text,
                    "level_id": level_id,
                    "description": webdecode_b64(level_data["levelDesc"].strip(), session),
                    "likes": int(level_data["likes"]),
                    "downloads": int(level_data["downloads"]),
                }
                return_levels.append(return_level_data)
                with open("processed", "w") as f:
                    f.write(f"{processed}, {level_name}")
    except TypeError as e:
        print(f"Error in job(process_levels), e: {e}, level_name: {level_name}")
    return return_levels


def generate_embed(data, processed: list, i: int) -> discord.Embed:
    level_name = data["level_name"]
    logger = change_log_format("main")
    logger.info(f"Sending message for level {level_name}. ({i + 1}/{len(processed[1:])})")
    author = data["author"]
    level_id = data["level_id"]
    difficulty = data["difficulty"]
    description = data["description"]
    downloads = data["downloads"]
    likes = data["likes"]
    embed = discord.Embed(
        title=f"GDPS RateBot version 1.3 - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}",
        description=f"""
# [Level was rated!](https://amber.ps.fhgdps.com/tools/stats/stats.php)
## Someone rated a level! <:star_1:1189758578165301338>

## **Level**
**{level_name}** by **{author}** 

## Level ID
{level_id} 

## Difficulty
{difficulty} 

## Level Stats
<:download:1190083854527103047> {downloads} | <:like:1190083855944798268> {likes}

## Description
{description if str(description).strip() != "" and description is not None else "None"}
""",
        color=0x0377fc
    )
    return embed


def webdecode_b64(encoded_str: str, session: requests.Session):
    url = 'https://amber.ps.fhgdps.com/b64.php'
    headers = {
        'User-Agent': 'GDPSRateBot/1.0'
    }
    response = session.get(url, params={'data': encoded_str}, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError(f"Error no. {response.status_code} ({response.text})")
