import discord.ext.commands
import requests
import json


def get_accounts(url: str, session: requests.Session) -> list[dict]:
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise WindowsError(f"Failed to get accounts, error {response.status_code} "
                           f"({response.text if not response.text.startswith('<!') else 'HTML response'})")


def save_account_data(data: list[dict]):
    with open("accounts.json", "w") as file:
        json.dump({"data": data}, file, indent=2)


def get_user_by_id(user_id=21, session: requests.Session = None) -> str:
    save_account_data(get_accounts("https://amber.ps.fhgdps.com/getAccounts.php", session))
    with open("accounts.json", "r") as file:
        opened = json.load(file)
    data = opened.get("data")
    for user in data:
        if user["userID"] == user_id:
            return f"Found user {user['userName']} with id {user_id}, data is WIP for this too."
        else:
            continue
    return f"Didnt file user by id {user_id}"
