import json
import requests
import discord


def create_discord_embed(data_dict, color=discord.Colour.blue()):
    actions = data_dict.get("Actions")
    actions = actions.split("\n")
    embed_desc = ""
    for i, action in enumerate(actions):
        action = action.replace("'", '"')
        if not len(action) < 10:
            actions[i] = json.loads(str(action))
    for action in actions:
        if str(action).strip() == "" or action is None:
            break
        moderator = action["Moderator"]
        action_str = action["Action"]
        value_1 = action["Value"]
        value_2 = action["Value2"]
        level_id = action["LevelID"]
        time = action["Time"]
        gen = f"""
            \nAction "{action_str}" at {time} by {moderator}, Level id: {level_id}, Value 1: {value_1}, Value 2: {value_2}
        """
        embed_desc = f"{embed_desc}{gen}"
    count = len(embed_desc.split("Action"))
    title = f'{count-1} Moderator Actions'
    return discord.Embed(title=title, description=embed_desc, colour=color)


def get_moderator_actions(session: requests.Session, url, count=5, max_description_length=800):
    response_actions = session.get(url, params={"count": count})
    data_actions = response_actions.json()
    description = ""

    try:
        for action in data_actions["actions"]:
            action_str = str(action)
            # Limit the length of each action to avoid exceeding Discord limit
            if len(description) + len(action_str) <= max_description_length:
                description += f"{action_str}\n"
            else:
                break  # Stop if the description is too long
    except KeyError:
        description = f"Failed to get moderator actions, received content: {response_actions.content.decode('utf-8')}"

    return create_discord_embed({"Actions": description})


def get_moderator_statistics_by_id(url, moderator_id, session: requests.Session):
    response_statistics_id = session  .get(url, params={"moderatorID": moderator_id})
    data_statistics_id = response_statistics_id.json()

    title = "Moderator Statistics by ID"
    return create_discord_embed(title, data_statistics_id["statistics"])


def get_moderator_statistics_by_name(url, moderator_name, session: requests.Session):
    response_statistics_name = session.get(url, params={"moderatorName": moderator_name})
    data_statistics_name = response_statistics_name.json()

    title = "Moderator Statistics by Name"
    return create_discord_embed(title, data_statistics_name["statistics"])
