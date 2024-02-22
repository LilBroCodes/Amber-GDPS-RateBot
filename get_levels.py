import requests
import json


def isfloat(s):
    s = s.strip()
    if s.startswith('-'):
        s = s[1:]
    return s.replace('.', '', 1).isdigit()


def get_levels(url: str, session: requests.Session) -> list[dict]:
    headers = {
        'User-Agent': 'GDPSRateBot/1.0'
    }
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise ConnectionError(f"Failed to get levels, error {response.status_code} "
                              f"({response.text if not response.text.startswith('<!') else 'HTML response'})")


def save_levels_data(data: list[dict]):
    with open("levels.json", "w") as file:
        json.dump({"data": data}, file, indent=2)
