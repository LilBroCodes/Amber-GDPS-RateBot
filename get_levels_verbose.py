import json

import requests

from gdlib import webdecode_b64
import discord
import datetime


def gen_level_embed(data: dict, verbose=False, session: requests.Session = None) -> discord.Embed:
    author = data["userName"]
    level_name = data["levelName"]
    description = webdecode_b64(data["levelDesc"], session)
    objects = data["objects"]
    coins = data["coins"]
    requested_stars = data["requestedStars"]
    upload_date = datetime.datetime.fromtimestamp(int(data["uploadDate"]), datetime.UTC)
    update_date = datetime.datetime.fromtimestamp(int(data["updateDate"]), datetime.UTC)
    rate_date = datetime.datetime.fromtimestamp(int(data["rateDate"]), datetime.UTC)
    has_coins = False if int(data["starCoins"]) == 1 else False
    featured = False if int(data["starFeatured"]) == 1 else False
    hall_of_fame = False if int(data["starHall"]) == 1 else False
    epic = False if int(data["starEpic"]) == 1 else False
    unlisted = False if int(data["unlisted"]) == 1 else False
    if verbose and not unlisted:
        generated_list = [f"\n**{key}: **{value}" for key, value in data.items()]
        generated = ""
        for string in generated_list:
            generated = f"{generated}{string}"
        if len(generated) >= 5000:
            generated = generated[:3000] + "(TOO LONG)"
        embed = discord.Embed(
            title=f"{level_name} by {author}",
            description=generated,
            colour=discord.Colour.blue()
        )
        return embed
    elif not verbose and not unlisted:
        embed = discord.Embed(
            title=f"{level_name} by {author}",
            description=f"""
                        **Uploaded: ** {upload_date}
                        **Updated: ** {update_date}
                        **Rated (date): ** {rate_date}
                        **Coins: ** {"rated, " if has_coins else "not rated, "}{coins}
                        **Requested stars: ** {requested_stars}
                        **Featured: ** {featured}
                        **In hall of fame: ** {hall_of_fame}
                        **Is epic: ** {epic}
                        **Object count: ** {objects}
                        **Description: ** {description}
            """,
            colour=discord.Colour.blue()
        )
        return embed
    else:
        return discord.Embed(
            title="Unlisted level.",
            description="# Level is unlisted."
        )
