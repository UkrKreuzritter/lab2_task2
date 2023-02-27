"""
Program works with clients requests
"""
from requests import post, get
import base64
import json
client_id="c348bc3c509d4f5c830431191e175b88"
client_secret="839d50a48a4d41f695003b6b6223be3c"
def get_token(client_id:str, client_secret:str) -> str:
    """
    Function gets_token
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def search_for_artist(token:str, artist:str) -> dict:
    """
    Function searches for artist
    """
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={artist}&type=artist&limit=1"
    result = get(url + query , headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        return "Nope"
    return json_result[0]
    
def search_artist_top_song(token:str, artist:str) -> dict:
    """
    Function searches for artist top song
    """
    url="https://api.spotify.com/v1/artists/"+search_for_artist(token, artist)["id"]+"/top-tracks"
    headers = {"Authorization": "Bearer " + token}
    query = f"?market=UA"
    result = get(url + query, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    if len(json_result) == 0:
        return "Nope"
    return json_result[0]

def get_avaliable_markets(token:str, artist:str) ->list:
    """
    Function searches for avaliable markets
    """
    url = "https://api.spotify.com/v1/tracks/" + search_artist_top_song(token, artist)["id"]
    headers = {"Authorization": "Bearer " + token}
    result = get(url , headers = headers)
    json_result = json.loads(result.content)
    return json_result["available_markets"]

if __name__ == "__main__":
    token = get_token(client_id, client_secret)
    print("Введіть назву виконавця чи гурту")
    artist = str(input(">>> "))
    command = ""
    print("Якщо захочете змінити назву групи, то напишіть change та назву групи у дужках")
    print("Для того, щоб перервати підневільний подвиг існування (покинути програму), необхідно написати esc")
    while command != "esc": 
        print("Введіть поле, про яке хочете більше дізнатися: artist | top_tracks | avaliable_markets")
        command = str(input(">>> "))
        if command == "artist":
            artist_data = search_for_artist(token, artist)
            command = ""
            while command != "id" and command != "name" and command != "esc":
                print("Введіть поле, про яке хочете більше дізнатися: id | name. Або esc")
                command = str(input(">>> "))
            if command == "id" or command == "name":
                print(artist_data[command])
        elif command == "top_tracks":
            song = search_artist_top_song(token, artist)
            command = ""
            while command != "id" and command != "name" and command != "esc":
                print("Введіть поле, про яке хочете більше дізнатися: id | name. Або esc")
                command = str(input(">>> "))
            if command == "id" or command == "name":
                print(song[command])
        elif command == "avaliable_markets":
            markets = get_avaliable_markets(token, artist)
            nums=[0, 0]
            while min(nums[0], nums[1]) < 1 or max(nums[0], nums[1]) > len(markets) or min(nums[0], nums[1]) != nums[0]:
                print("Тут всього ", len(markets), "країн. Напишіть проміжок у форматі l:r (рахунок від 1). Або esc")
                command = str(input(">>> "))
                if command == "esc":
                    break
                nums = command.split(":")
                nums = (int(nums[0]), int(nums[1]))     
            if command != 'esc':
                print(markets[nums[0]+1:nums[1]])
        if command.find("change") != -1:
            artist = command[command.find("(") + 1: command.find(")")]
        