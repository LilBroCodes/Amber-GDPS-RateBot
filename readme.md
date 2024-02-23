# GDPS-Ratebot

GDPS-Ratebot is a Discord bot designed to provide various functionalities related to Geometry Dash Private Servers (GDPS), including retrieving account information, level data, and moderation actions.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Introduction

GDPS-Ratebot is developed to streamline interactions with Geometry Dash Private Servers through Discord. It provides easy access to account details, level information, moderation actions, and more, enhancing the overall experience for users within the Geometry Dash community.

## Features

- Retrieval of account information by ID.
- Display of level data including difficulty and other details.
- Audit of moderation actions on the GDPS.
- Play audio from YouTube in a voice channel.
- Integration with giveaways (WIP).

## Installation

To install GDPS-Ratebot, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Obtain a Discord bot token and a YouTube Data API key.
4. Run the bot using `python bot.py <channel_id> <bot_token>` where `<channel_id>` is the ID of the Discord channel where the bot will operate and `<bot_token>` is your Discord bot token.

## Usage

Once installed and running, GDPS-Ratebot operates within the designated Discord server. Users can interact with the bot by sending commands prefixed with `--`. For example, `--get_level <id>` retrieves data about a specific level identified by `<id>`.

## Commands

- `--get-acc-by-id <id>`: Retrieves account data based on the provided ID.
- `--gdps-audit <count>`: Displays recent moderation actions on the GDPS.
- `--get-level <id>`: Retrieves data of the level identified by the given ID.
- `--play <link>`: Plays audio from the provided YouTube link in a voice channel.
- `--leave`: Forces the bot to leave the voice channel.
- `--giveto <member> <giveaway>`: Adds a member to the specified giveaway.
- `--list-people <giveaway>`: Lists members participating in the specified giveaway.

## Contributing

Contributions to GDPS-Ratebot are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request. Please follow the existing code style and conventions.

## License

This project is licensed under the CCO-1.0 License - see the [LICENSE](LICENSE) file for details.
