from spotipy.oauth2 import SpotifyClientCredentials
import spotipy, json, re
from operator import itemgetter
from collections import Counter
import requests

#Magically makes a URL into a URI
#Because we know someone is going to put in a URL
def url_to_uri(url):
    #strip everything before playlist/ and everything after ?
    try:
        if "http" in url and "playlist/" in url:
            try:
                uri = str(url).split("playlist/")[1].split("?")[0]
                return uri
            except:
                return None
        else:
            return None
    except:
        return None

def profileurl(url):
    try:
        if "http" in url and "user/" in url and "open.spotify.com" in url:
            try:
                user = str(url).split("user/")[1].split("?")[0]
                return user
            except:
                return None
        else:
            return "No such user exists"
    except:
        return None
        
#Gets authentication for the app from another file somewhere...
def getClient():
    stuff = []
    with open("auth", "r") as f:
        for line in f.readlines():
            stuff.append(line.strip('\n'))
    return stuff

def main(uri):
    artists = []
    cl = getClient()
    client_credentials_manager = SpotifyClientCredentials(cl[0], cl[1])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    username = uri.split(':')[2]
    playlist_id = uri.split(':')[3]

    if playlist_id == "None" or playlist_id == None:
        return None

    #Queries the total tracks in a playlist
    #Checks if real playlist
    try:
        results = sp.user_playlist_tracks(user=username, playlist_id=playlist_id)
    except spotipy.client.SpotifyException:
        return None
    except requests.exceptions.ConnectionError:
        return "Connection Error"

    totalTracks = results['total']
    trackIndex = 0

    #While the index is less than the total tracks, set the offset to the index and get the artists' names from there
    #Kind of bypasses the limit of 100
    while trackIndex < int(totalTracks):
        r = sp.user_playlist_tracks(username, playlist_id=playlist_id, offset=trackIndex)
        for track in r['items']:
            artists.append(track['track']['album']['artists'][0]['name'])
        trackIndex += 100
        
    a = {}
    c = Counter(artists)
    for artist in c:
        percent = format((c[artist]/totalTracks)*100, '.2f')
        a.update({artist : c[artist]})

    return a
    
def compare(uriA, uriB):
    tracklistA = []
    tracklistB = []

    cl = getClient()
    client_credentials_manager = SpotifyClientCredentials(cl[0], cl[1])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    usernameA = uriA.split(':')[2]
    playlist_idA = uriA.split(':')[3]
    usernameB = uriB.split(':')[2]
    playlist_idB = uriB.split(':')[3]

    if playlist_idA == "None" or playlist_idA == None or playlist_idB == "None" or playlist_idB == None:
        return None
    try:
        resA = sp.user_playlist_tracks(user=usernameA, playlist_id=playlist_idA)
        resB = sp.user_playlist_tracks(user=usernameB, playlist_id=playlist_idB)
    except spotipy.client.SpotifyException:
        return None
    except requests.exceptions.ConnectionError:
        return "Connection Error"

    trackIndexA, trackIndexB = 0, 0
    totalTracksA, totalTracksB = resA["total"], resB["total"]

    while trackIndexA < int(totalTracksA):
        r = sp.user_playlist_tracks(usernameA, playlist_id=playlist_idA, offset=trackIndexA)
        for track in r['items']:
            #Make dict with album name, track name, and artist name
            #track["track"]["name"]
            #track["track"]["album"]["name"]
            #track["track"]["album"]["artists"][0]["name"]
            tracklistA.append(
                {
                    "artist" : track["track"]["album"]["artists"][0]["name"],
                    "track" : track["track"]["name"],
                    "album" : track["track"]["album"]["name"],
                    "imgurl" : track["track"]["album"]["images"][0]["url"]
                }
            )
        trackIndexA += 100
    while trackIndexB < int(totalTracksB):
        r = sp.user_playlist_tracks(usernameB, playlist_id=playlist_idB, offset=trackIndexB)
        for track in r['items']:
            #Make dict with album name, track name, and artist name
            #track["track"]["name"]
            #track["track"]["album"]["name"]
            #track["track"]["album"]["artists"][0]["name"]
            tracklistB.append(
                {
                    "artist" : track["track"]["album"]["artists"][0]["name"],
                    "track" : track["track"]["name"],
                    "album" : track["track"]["album"]["name"],
                    "imgurl" : track["track"]["album"]["images"][0]["url"]
                }
            )
        trackIndexB += 100

    return [val for val in tracklistA if val in tracklistB]