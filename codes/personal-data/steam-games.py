import csv
import requests
import codecs
import time
import sys

API_KEY = sys.argv[1]
PROFILE = sys.argv[2]

HEADER = [
    "appid",
    "name",
    "playtime_forever",
    "img_icon_url",
    "img_logo_url",
    "playtime_windows_forever",
    "playtime_mac_forever",
    "playtime_linux_forever",
    "achievements",
    "total_achievements",
    "earned_achievements"
]

r = requests.get(
    'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={profile}&format=json&include_played_free_games=true&include_appinfo=true'.format(
        api_key=API_KEY,
        profile=PROFILE
    ))

if r.status_code != 200:
    print(r.text)
    print("Wait to make the requests!")
    exit(0)

games = r.json()['response']['games']

with codecs.open('steam_games.csv', 'w', "utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=HEADER)
    writer.writeheader()
    i = 1
    for game in games:
        print('{num} of {total}'.format(num=i, total=len(games)))
        i += 1
        not_worked = True
        while not_worked:
            not_worked = False
            time.sleep(2)
            r = requests.get(
                'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={api_key}&steamid={steamid}'.format(
                    api_key=API_KEY,
                    app_id=game['appid'],
                    steamid=PROFILE
                )
            )
            if not r.status_code in [200, 400]:
                not_worked = True
        
        json_r = r.json()['playerstats']
        achievements = json_r['achievements'] if 'achievements' in json_r else []
        total = 0
        earned_ach = 0
        for achievement in achievements:
            total += 1
            if achievement['achieved']:
                earned_ach += 1

        game["achievements"] = earned_ach / total if total else None
        game["total_achievements"] = total
        game["earned_achievements"] = earned_ach
        game = {key: game[key] for key in HEADER}
        writer.writerow(game)
