#!/usr/bin/env python3
#Goal is to get all the roguelike games from my steam library, get the name, release date, rating, my hours played,
#and price on steam, and display it in a table on my web page.

import http.client
import json
import operator
#Set up http client to steam web api
steamHost = "api.steampowered.com"
steamConn = http.client.HTTPSConnection(steamHost)

#Set up http client to steamspy
spyHost = "steamspy.com"
spyConn = http.client.HTTPSConnection(spyHost)

#Open file with steam token, copy to variable, add token to URL
file = open("steamtoken", "r")
token = file.read()
file.close()
ownedGamesURL = "/IPlayerService/GetOwnedGames/v1/?access_token={}&steamid=76561198275885590&include_appinfo=true&include_extended_appinfo=false"
ownedGamesURL = ownedGamesURL.format(token)
#Request owned games from server, get a json response, read response and print some info.

steamConn.request("GET", ownedGamesURL, headers={"Host": steamHost})
response = steamConn.getresponse()
print(response.status, response.reason)
gamesOwnedResponse = json.loads(response.read())

#TODO: filter games by hrs played, print to file the list of games in that order.
#CHALLENGE: Make this take in any kind of game tag, and grab that instead of just roguelikes. and accept an amount from CLI
class Game:
    def __init__(self, game_info, spy_response):
        self.icon = "http://media.steampowered.com/steamcommunity/public/images/apps/{APPID}/{IMG_ICON_URL}.jpg"
        self.icon = self.icon.format(APPID=game_info["appid"], IMG_ICON_URL=game_info["img_icon_url"])
        self.title = game_info["name"]
        self.score = (1-(spy_response["negative"]/(spy_response["positive"]+spy_response["negative"])))*100
        self.hrs_played = (game_info["playtime_windows_forever"] + game_info["playtime_mac_forever"] + game_info["playtime_linux_forever"] + game_info["playtime_deck_forever"])
        self.hrs_played = (self.hrs_played / 60)
        self.price = int(spy_response["price"])/100


def add_if_has_tag(gameinfo,list):
    appID = gameinfo["appid"]
    #Request tag list from a appID
    tagListURL = "/api.php?request=appdetails&appid={}"
    tagListURL = tagListURL.format(appID)
    spyConn.request("GET", tagListURL, headers={"Host": spyHost})
    response = spyConn.getresponse()
    print(response.status, response.reason)
    try:
        spyResponse = json.loads(response.read())
    except:
        return
    

    for x in spyResponse["tags"]:
        if x == desired_tag:
            list.append(Game(gameinfo, spyResponse))
            return

grabbed_games = []
#What tag would to like to sort games by?
desired_tag = "Rogue-like"
num_games_wanted = 0

print("Make sure to spell tags correctly or this won't work. For a full list of tags go to: 'https://steamdb.info/tags/'")
desired_tag = input("What tag would you like to sort by? ")
num_games_wanted = int(input("How many games would you like to get? (Games are sorted by highest hours played descending.) "))

for x in gamesOwnedResponse["response"]["games"]:
    length = len(grabbed_games)
    add_if_has_tag(x, grabbed_games)
    if length != len(grabbed_games):
        print("added: ", grabbed_games[length].title)

grabbed_games.sort(key=operator.attrgetter("hrs_played"), reverse=True)
file = open("gamelist.html", "w")
if num_games_wanted < 1:
    for game in grabbed_games:
        file.write(
        """
        <tr>
        <td><img src="{icon}" class="table-icon" alt="{gametitle} icon"/></td>
        <td>{gametitle}</td>
        <td>{score}</td>
        <td>{hrsplayed}</td>
        <td>{price}</td>
        </tr>
        """.format(
                icon = game.icon, 
                gametitle = game.title,
                score = f"{game.score:.1f}", 
                hrsplayed = f"{game.hrs_played:.2f}",
                price = f"{game.price:.2f} USD"
            )
        )
else:
    for game in grabbed_games[:num_games_wanted]:
        file.write (
            """
            <tr>
            <td><img src="{icon}" class="table-icon" alt="{gametitle} icon"/></td>
            <td>{gametitle}</td>
            <td>{score}</td>
            <td>{hrsplayed}</td>
            <td>{price}</td>
            </tr>
            """.format(
                    icon = game.icon, 
                    gametitle = game.title,
                    score = f"{game.score:.1f}", 
                    hrsplayed = f"{game.hrs_played:.2f}",
                    price = f"{game.price:.2f} USD"
                )
        )

