# Auto send message to discord channel via web request
import requests

from _secret import discord_web_Auth


def send_msg_to_discord_request(msg, channel_id=1224936399766032404, auth=discord_web_Auth):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    payload = {
        "content": msg,
    }

    header = {
        'Authorization': auth,
    }

    r = requests.post(url, data=payload, headers=header)

    print(r)

