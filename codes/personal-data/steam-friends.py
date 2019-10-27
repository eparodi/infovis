import csv
import requests
import codecs
import time
import sys

API_KEY = sys.argv[1]
PROFILE = sys.argv[2]

HEADER = [
    'steamid',
    'relationship',
    'friend_since',
    'avatarfull',
    'communityvisibilitystate',
    'personaname',
    'profileurl',
    'lastlogoff',
]

r = requests.get(
    'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={profile}&relationship=all'.format(
        api_key=API_KEY,
        profile=PROFILE
    ))

if r.status_code != 200:
    print("Wait to make the requests!")
    exit(0)

friends = r.json()['friendslist']['friends']

with codecs.open('steam_friends.csv', 'w', "utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=HEADER)
    writer.writeheader()
    i = 1
    for friend in friends:
        print('{num} of {total}'.format(num=i, total=len(friends)))
        i += 1
        not_worked = True
        while not_worked:
            not_worked = False
            time.sleep(2)
            r = requests.get(
                'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamid}'.format(
                    api_key=API_KEY,
                    steamid=friend['steamid']
                )
            )
            if r.status_code != 200:
                not_worked = True

        profile = r.json()['response']['players'][0]
        for key in HEADER:
            if key in profile.keys():
                friend[key] = profile[key]
        writer.writerow(friend)
