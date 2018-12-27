import json
import requests
from matrix_client.client import MatrixClient

# TODO: Move to config file
botname = "susi"
susi_api = "https://api.susi.ai/susi/chat.json"

client = MatrixClient("https://amorgan.xyz",
             token="MDAxOWxvY2F0aW9uIGFtb3JnYW4ueHl6CjAwMTNpZGVudGlmaWVyIGtleQowMDEwY2lkIGdlbiA9IDEKMDAyNGNpZCB1c2VyX2lkID0gQHN1c2k6YW1vcmdhbi54eXoKMDAxNmNpZCB0eXBlID0gYWNjZXNzCjAwMjFjaWQgbm9uY2UgPSBZenIqc2EjWnlxV3VsRDl2CjAwMmZzaWduYXR1cmUgNIN3J7wUrya0LX7FfWXXsc7eKqTMTMD8IiKwKADZq2MK",
             user_id="@susi:amorgan.xyz")

# Cache room list locally
rooms = client.get_rooms()

def susi_submit(msg):
    """Given a request, return susi's response"""
    r = requests.get(susi_api + "?timezoneOffset=0&q=" + msg.replace(" ", "+"))
    response = json.loads(r.content)
    if len(response["answers"]) > 0 and len(response["answers"][0]["actions"]) > 0:
        return response["answers"][0]["actions"][0]["expression"]
    return "Ask again later"

def invite_received(room_id, state):
    """Received a room invite. Join the room."""
    print("Joining:", room_id)
    client.join_room(room_id)

    # Update room dict
    rooms = client.get_rooms()

def message_received(event):
    """Received a room message. Check if for us and respond if so."""
    content = event["content"]
    if content["msgtype"] == "m.text":
        if content["body"].startswith(botname):
            query = content["body"][5:]
            rooms[event["room_id"]].send_text(susi_submit(query))

# Listen for invites and join room
client.add_invite_listener(invite_received)

# Listen for bot requests and respond
client.add_listener(message_received, "m.room.message")
print("Listening")
client.listen_forever()
