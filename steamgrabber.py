#Goal is to get all the roguelike games from my steam library, get the name, release date, rating, my hours played,
#and price on steam, and display it in a table on my web page.
#Steam Web API: 
#GetOwnedGames: returns appID and game name.
#GetTagList: enter appID, return tag list, check for tag:'roguelike'
import http.client
import json
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

def writeIfRoguelike(gameinfo,file):
    appID = gameinfo["appid"]
    #Request tag list from a appID
    tagListURL = "/api.php?request=appdetails&appid={}"
    tagListURL = tagListURL.format(appID)
    spyConn.request("GET", tagListURL, headers={"Host": spyHost})
    response = spyConn.getresponse()
    #print(response.status, response.reason)
    spyResponse = json.loads(response.read())

    for x in spyResponse["tags"]:
        if x == "Rogue-like":
            score = spyResponse["negative"]/(spyResponse["positive"]+spyResponse["negative"])
            score = (1-score)*100
            file.write(
                """
                <tr>
                <td>{icon}</td>
                <td>{gametitle}</td>
                <td>{score}</td>
                <td>{hrsplayed}</td>
                <td>{price}</td>
                </tr>
                """.format(icon="",gametitle=gameinfo["name"], score=score, hrsplayed=gameinfo["playtime_windows_forever"], price=spyResponse["price"])
            )
            return
file = open("gamelist.html", "w")
for x in gamesOwnedResponse["response"]["games"]:
    writeIfRoguelike(x, file)

#file = open("gamelist.html", "w")
#check game for roguelike tag, if it has that tag, add to a list of games.
#for x in spyResponse["tags"]:
#    
        



#grab Title,IconIMG Rating, MyHoursPlayed, Price.

#add game info to dictionary

#somehow display this information as a table.
