import requests  # calling web service

import jsons  # relational-object mapping

import uuid
import pathlib
import logging
import sys
import base64
import time
from configparser import ConfigParser

client_id = "cc14b21f2a9b4e36afe72e9e2268251b"
client_secret = "42abbb5568ad4dffb4ee3986e8765d08"

###################################################################
#
# start_menu
#
def start_menu():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """

  try:
    print()
    print(">> Enter a command:")
    print("   0 => Exit")
    print("   1 => Sign in")
    print("   2 => Create Account/Update Info")

    cmd = int(input())
    return cmd

  except Exception as e:
    print("ERROR")
    print("ERROR: invalid input")
    print("ERROR")
    return -1

###################################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """

  try:
    print()
    print(">> Enter a command:")
    print("   0 => Log Out")
    print("   1 => Top 10 Songs from Artist")
    print("   2 => Get Recommendations (DEPRECATED AND NO LONGER WORKS)")
    print("   3 => Add Favorite Songs")
    print("   4 => Delete Favorite Song")
    print("   5 => View Favorite Songs")
    print("   6 => Calculate song time")
    print("   7 => Calculate Genre Stats")

    cmd = int(input())
    return cmd

  except Exception as e:
    print("ERROR")
    print("ERROR: invalid input")
    print("ERROR")
    return -1
  
###################################################################
#
# recommend_menu
#
def recommend_menu():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """

  try:
    print()
    print(">> Enter a command:")
    print("   0 => Back")
    print("   1 => Add a genre")
    print("   2 => Add an artist")
    print("   3 => Delete an input")
    print("   4 => Print inputs")
    print("   5 => Confirm")

    cmd = int(input())
    return cmd

  except Exception as e:
    print("ERROR")
    print("ERROR: invalid input")
    print("ERROR")
    return -1

###################################################################
#
# get_token
#
def get_token():
    """
    Gets the token needed for the API
    
    Parameters
    ----------
    None
    
    Returns
    -------
    Token
    """
    try:
        auth_string = client_id + ":" + client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        res = requests.post(url, headers=headers, data=data)
        body = res.json()
        token = body["access_token"]
        return token

    except Exception as e:
        logging.error("get_token failed:")
        logging.error("url: " + url)
        logging.error(e)
        return

###################################################################
#
# get_auth_headers
#
def get_auth_headers(token):
    """
    helper function to format the headers using token
    
    Parameters
    ----------
    Token
    
    Returns
    -------
    Headers Parameter
    """
    return {"Authorization": "Bearer " + token}

###################################################################
#
# get_artist_info
#
def get_artist_info(token, artist_search):
    """
    Helper function to get an artist's id number and name using a search
    
    Parameters
    ----------
    token, artist_name
    
    Returns
    -------
    tuple (id, name)
    """
    try:
        # Build web call
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_headers(token)
        query = f"?q={artist_search}&type=artist&limit=1"
        query_url = url + query
        res = requests.get(query_url, headers=headers)

        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            #
            return

        body = res.json()["artists"]["items"]
        if len(body) == 0:
            print("No such artist exists...")
            return None
        
        artist_id = body[0]["id"]
        artist_name = body[0]["name"]
        return artist_id, artist_name

    except Exception as e:
        logging.error("upload() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return

###################################################################
#
# get_genres
#
def get_genres(token):
    """
    Helper function to print all genres of music
    
    Parameters
    ----------
    token
    
    Returns
    -------
    None
    """
    try:
        # Build web call
        url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        headers = get_auth_headers(token)
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return

        # JSON of all genres
        body = res.json()["genres"]
        for genre in body:
            print(genre)
        return 

    except Exception as e:
        logging.error("upload() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return

###################################################################
#
# get_songs_by_artist
#
def get_songs_by_artist(token):
    """
    Get the top 10 songs by an artist input by a user.
    
    Parameters
    ----------
    token
    
    Returns
    -------
    None
    """
    try:
        artist_search = input("Enter artist name: ")
        artist_id, artist_name = get_artist_info(token, artist_search)

        #Call webservice
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        headers = get_auth_headers(token)
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            #
            return

        #Json of tracks
        tracks = res.json()["tracks"]
        
        # Name correction for misspell
        if artist_search.lower() != artist_name.lower():
            print(f"Top 10 songs for '{artist_search}'. Did you mean {artist_name}?")
        else:
            print(f"Top 10 songs for '{artist_name}'.")

        # Print out top 10 tracks
        for idx, song in enumerate(tracks):
            print(f"{idx + 1}. {song['name']}")
        return

    except Exception as e:
        logging.error("upload() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return
    
###################################################################
#
# get_recommendations
#
def get_recommendations(baseurl, token):
    """
    Send user inputs for recommendations to the server.
    """
    try:
        print("404 Error: Recommendations gateway depricated... Feel free to look at code though")
        return
        genres = []
        artists = []
        inputs = []
        print("Getting recommendations requires up to 5 inputs of genres and/or artists.")

        while True:
            cmd = recommend_menu()

            #------------------------------- BUILD RECOMMENDATION INPUTS -------------------------------#

            if cmd == 1:  # Add genres
                while len(inputs) < 5:
                    # In case user needs list of genres
                    if input('Would you like to see all genres? (y/n): ') == 'y':
                        get_genres(token)
                    genre = input(f"Enter genre (or type 'done' to finish). Input {len(inputs) + 1} of 5: ").strip()
                    if genre.lower() == "done":
                        break
                    genres.append(genre)
                    inputs.append(genre)

            elif cmd == 2:  # Add artists
                while len(inputs) < 5:
                    artist = input(f"Enter artist name (or type 'done' to finish). Input {len(inputs) + 1} of 5: ").strip()
                    if artist.lower() == "done":
                        break
                    artists.append(artist)
                    inputs.append(artist)

            elif cmd == 3:  # Delete inputs
                print("Current inputs:")
                for i, item in enumerate(inputs, start=1):
                    print(f"{i}: {item}")
                delete = input("Enter the number of the input to delete (or 'cancel' to go back): ").strip()
                if delete.lower() == "cancel":
                    continue
                try:
                    delete_idx = int(delete) - 1
                    if 0 <= delete_idx < len(inputs):
                        removed_item = inputs.pop(delete_idx)
                        if removed_item in genres:
                            genres.remove(removed_item)
                        else:
                            artists.remove(removed_item)
                        print(f"Removed: {removed_item}")
                        print(f"New inputs: {inputs}")
                    else:
                        print("Invalid number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            elif cmd == 4:  # Print inputs
                print("Current inputs:")
                if not inputs:
                    print("No inputs yet.")
                else:
                    for i, item in enumerate(inputs, start=1):
                        print(f"{i}: {item}")

            #------------------------------- SEND INPUT TO SERVER -------------------------------#
            elif cmd == 5:  # Confirm and get recommendations
                if not inputs:
                    print("No inputs provided. Please add at least one genre or artist.")
                    continue

                # Build the data packet
                data = {
                    "token": token,
                    "genres": genres,
                    "artists": artists,
                }

                # Call the web service
                api = '/recommendations'
                url = baseurl + api

                res = requests.get(url, json=data)

                #------------------------------- DISPLAY OUTPUT -------------------------------#

                if res.status_code == 200:
                    body = res.json()
                    if body["success"]:
                        print("Recommendations:")
                        for rec in body["recommendations"]:
                            print(f"- {rec['name']} by {', '.join(rec['artists'])}")
                            print(f"  Listen here: {rec['url']}")
                        return
                    else:
                        print("Failed to get recommendations:", body["message"])
                else:
                    print("Failed with status code:", res.status_code)
                    print("Error message:", res.json().get("message", "Unknown error"))
                return

            #------------------------------- CANCEL FUNCTION -------------------------------#
            elif cmd == 0:  # Back
                print("Exiting recommendation system.")
                break

            else:
                print("Invalid command. Please try again.")

    except Exception as e:
        logging.error("get_recommendations() failed:")
        logging.error('url: ')
        logging.error(e)

###################################################################
#
# add_user
#
def add_user(baseurl):
    """
    Prompts the user for the new user's username, password,
    email, last name, and first name, and then inserts this user into the database.
    If the user's email already exists in the database, then update the user's info.

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    True/False
    """

    try:
        print("Enter user's email>")
        email = input()

        print("Enter user's last (family) name>")
        last_name = input()

        print("Enter user's first (given) name>")
        first_name = input()

        print("Create a username>")
        username = input()

        print("Create a password>")
        password = input()

        # Build the data packet
        data = {
            "email": email,
            "lastname": last_name,
            "firstname": first_name,
            "username": username,
            "password": password 
        }

        # Call the web service
        api = '/new_user'
        url = baseurl + api

        retries = 3
        attempt = 0

        while attempt < retries:
            try:
                res = requests.put(url, json=data)
                if res.status_code != 200:
                    print("Failed with status code:", res.status_code)
                    if res.status_code in [400, 500]:
                        body = res.json()
                        print("Error message:", body.get("message", ""))
                    break

                body = res.json()
                userid = body["userid"]
                message = body["message"]

                print("User", userid, "successfully", message)
                return True

            except Exception as e:
                attempt += 1
                print(f"Attempt {attempt} failed. Retrying...")
                time.sleep(3)

        print("Max retries reached. Could not complete request.")
        return False
    except Exception as e:
        logging.error("add_user() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return False

###################################################################
#
# sign_in
#
def sign_in(baseurl):
    """
    Prompts the user for username and password,
    then verifies their credentials with the backend.
    Allows up to 3 retries

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    True/False
    """
    attempts = 0
    while attempts < 3:
        try:
            print("Enter your username>")
            username = input()

            print("Enter your password>")
            password = input()

            # Build the data packet
            data = {
                "username": username,
                "password": password
            }

            # Call the web service
            api = '/signin'
            url = baseurl + api

            res = requests.post(url, json=data)

            if res.status_code == 200:
                body = res.json()
                userid = body.get("userid")
                
                if userid:
                    print("Sign-in successful! Welcome,", username)
                    return True, username, userid
                else:
                    print("Invalid username or password.")
            else:
                print("Sign-in failed with status code:", res.status_code)
                body = res.json()
                print("Error message:", body.get("message", ""))
                return False

        except Exception as e:
            logging.error("sign_in() failed:")
            logging.error('url: ' + url)
            logging.error(e)
            return False

        attempts += 1
        print(f"Attempt {attempts} of 3 failed. Please try again.")
    
    print("Maximum sign-in attempts exceeded. Please try again later.")
    return False

###################################################################
#
# add_song
#
def add_song(baseurl, userid, token):
    """
    Search for a song by title, display the top five matches, 
    let the user select one, and save it to the favorites table.
    Parameters
    ----------
    baseurl: baseurl for web service
    userid: user's userid
    token: token for Spotify API

    Returns
    -------
    None
    """
    try:
        print("Search for a song by title or artist.")
        song_title = input("Enter the song title to search: ").strip()

        if not song_title:
            print("No title entered. Exiting song search.")
            return None  # Exit without storing any data

        # Build the data packet for search
        search_data = {
            "token": token,
            "query": song_title,
        }

        # Call the web service to search for the song
        api = '/search_song'
        url = baseurl + api

        res = requests.post(url, json=search_data)

        # Failed:
        if res.status_code != 200:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return None
        
        # Sucess:
        search_body = res.json()
        if search_body["success"]:
            # Display the search results
            print("Search Results:")
            songs = search_body["songs"]
            for i, song in enumerate(songs, start=1):
                print(f"{i}. {song['name']} by {song['artists']}")
            print("11. Cancel selection")

            # Prompt the user to select a song
            while True:
                try:
                    choice = int(input("Select a song by entering its number (1-11): ").strip())
                    if choice == 11:
                        print("Selection canceled.")
                        return None  # Exit without storing any data
                    elif 1 <= choice <= 10:
                        selected_song = songs[choice - 1]
                        track_id = selected_song.get("id")
                        track_title = selected_song.get("name")
                        track_artist = selected_song.get("artists")
                        track_genres = selected_song.get("genres")
                        print(f"You selected: {track_title} by {track_artist}")

                        # Prepare data for adding to favorites
                        favorite_data = {
                            "songid": track_id,
                            "userid": userid,
                            "songname": track_title,
                            "artistname": track_artist,
                            "genres": track_genres
                        }

                        # Send the favorite song to the backend
                        api = '/add_song'
                        url = baseurl + api
                        res = requests.post(url, json=favorite_data)

                        # Failed:
                        if res.status_code != 200:
                            print("Failed with status code:", res.status_code)
                            print("url: " + url)
                            if res.status_code in [400, 500]:  # we'll have an error message
                                body = res.json()
                                print("Error message:", body["message"])
                            return None
                        
                        # Sucess:
                        fav_body = res.json()
                        if fav_body.get("success"):
                            print("Song successfully added to favorites.")
                            return {"track_id": track_id, "title": track_title}
                        else:
                            print("Failed to add song to favorites:", fav_body.get("message"))
                    
                        return None  # Exit after attempting to add to favorites
                    else:
                        print("Invalid choice. Please enter a number between 1 and 6.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        else:
            print("Failed to search for songs:", search_body.get("message"))


    except Exception as e:
        logging.error("add_song() failed:")
        logging.error('url: ' + url)
        logging.error(e)

###################################################################
#
# add_song
#
def delete_song(baseurl, userid):
    """
    Request to server to delete a song.

    Parameters
    ----------
    baseurl: baseurl for web service
    userid: user's userid

    Returns
    -------
    None
    """
    try:
        print("ENTERING DELETE SONG")
        songinfo = get_songs(baseurl, userid, True)

        # If the user canceled
        if songinfo is None:
            print("Song deletion canceled.")
            return

        # Build the data packet for search
        data = {
            "userid": userid,
            "songname": songinfo[0],
            "artistname": songinfo[1]
            
        }

        # Call the web service to calculate total time
        api = '/delete_song'
        url = baseurl + api

        res = requests.delete(url, json=data)

        # Failed:
        if res.status_code != 200:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return None
        
        # Sucess:
        print(f"{songinfo[0]} by {songinfo[1]} successfully deleted")
        return None
    
    except Exception as e:
        logging.error("calc_time() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return
###################################################################
#
# calc_time
#
def calc_time(baseurl, userid, token):
    """
    Request to server to calculate the total amount of time of music from
    favorited songs
    """
    try:
        # Build the data packet for search
        data = {
            "token": token,
            "userid": userid
        }

        # Call the web service to calculate total time
        api = '/calc_time'
        url = baseurl + api

        res = requests.get(url, json=data)

        # Failed:
        if res.status_code != 200:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return None
        
        # Sucess:
        total_duration = res.json().get("total_duration", 0)
        print(f"Total Duration: {total_duration} hours: minutes: seconds")
        return total_duration

    
    except Exception as e:
        logging.error("calc_time() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return

###################################################################
#
# get_songs
#
def get_songs(baseurl, userid, select):
    """
    Lists out all the songs currently favorited, including artist names.

    Parameters
    ----------
    baseurl: baseurl for web service
    userid: userid of the user
    select: bool to indicate if we are selecting a song

    Returns
    -------
    Tuple (songname, artistname)
    or None
    """
    try:
        data = {
            "userid": userid
        }

        api = '/get_songs'
        url = baseurl + api

        res = requests.get(url, json=data)

        # Failed:
        if res.status_code != 200:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return None

        # Success:
        result = res.json()

        songs = result.get("songs", [])
        if songs:
            print("Favorite Songs:")
            for i, song in enumerate(songs, start=1):
                print(f"{i}. \"{song['songname']}\" by {song['artistname']}")

            if select:
                # Add the "Cancel deletion" option after listing songs
                print(f"{len(songs) + 1}. Cancel deletion")
                while True:
                    try:
                        selection = int(input("Which song do you want to delete? (enter a number): "))
                        if 1 <= selection <= len(songs):
                            selected_song = songs[selection - 1]
                            return selected_song['songname'], selected_song['artistname']
                        elif selection == len(songs) + 1:
                            return None
                        else:
                            print(f"Invalid selection. Please enter a number between 1 and {len(songs)}.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
        else:
            print("No favorite songs found.")
            return None

    except Exception as e:
        logging.error("get_songs() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return

###################################################################
#
# calc_genres
#
def calc_genres(baseurl, userid):
    """
    Fetches top 5 genres calculated by the server.

    Parameters
    ----------
    baseurl: baseurl for web service
    userid: userid of the user

    Returns
    -------
    None
    """
    try:
        data = {"userid": userid}
        api = "/calc_genres"
        url = baseurl + api

        res = requests.get(url, json=data)

        # Failed:
        if res.status_code != 200:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code in [400, 500]:
                body = res.json()
                print("Error message:", body["message"])
            return None

        # Success:
        res = res.json()
        if not res["success"]:
            print("Failed to get genre stats:", res.get("message"))
            return None

        # Display the top 5 genres
        top_genres = res.get("topGenres", [])
        print("Top 5 Genres:")
        for genre_info in top_genres:
            print(f"{genre_info['genre']}: {genre_info['count']} times")

    except Exception as e:
        logging.error("calc_genres() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return



#########################################################################
# main
#
print('** Welcome to MusicApp **')
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
config_file = 'musicapp-client-config.ini'

print("What config file to use for this session?")
print("Press ENTER to use default (musicapp-client-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
  pass  # already set
else:
  config_file = s

#
# does config file exist?
#
if not pathlib.Path(config_file).is_file():
  print(f"**ERROR: config file ' {config_file} ' does not exist, exiting")
  sys.exit(0)

#
# setup base URL to web service:
#
configur = ConfigParser()
configur.read(config_file)
baseurl = configur.get('client', 'webservice')

#
# make sure baseurl does not end with /, if so remove:
#
if len(baseurl) < 16:
  print("**ERROR**")
  print("**ERROR: baseurl '", baseurl, "' in .ini file is empty or not nearly long enough, please fix")
  sys.exit(0)

if baseurl.startswith('https'):
  print("**ERROR**")
  print("**ERROR: baseurl '", baseurl, "' in .ini file starts with https, which is not supported (use http)")
  sys.exit(0)

lastchar = baseurl[len(baseurl) - 1]
if lastchar == "/":
  baseurl = baseurl[:-1]

# print(baseurl)

#
# main processing loop:
#
def main():
    token = get_token()
    while True:
        cmd = start_menu()

        if cmd == 0:  # Exit
            print("Exiting MusicApp. Goodbye!")
            break

        elif cmd == 1:  # Sign in
            user = sign_in(baseurl)
            if user[0]:
                # Successful sign-in, proceed to main options
                userid = user[2]
                user = user[1]

                print(f"USER: {user}")
                while True:
                    user_cmd = prompt()
                    if user_cmd == 0:  # Exit application
                        print("Goodbye!")
                        break
                    elif user_cmd == 1:  # Top 10 songs by artist
                        get_songs_by_artist(token)
                    elif user_cmd == 2:  # Get recommendations
                        get_recommendations(baseurl, token)
                    elif user_cmd == 3:  # Add favorite songs
                        add_song(baseurl, userid, token)
                    elif user_cmd == 4:  # Delete favorite songs
                        delete_song(baseurl, userid)
                    elif user_cmd == 5:  # Print favorited songs
                        get_songs(baseurl, userid, False)
                    elif user_cmd == 6:  # Calculate total time of songs
                        calc_time(baseurl, userid, token)
                    elif user_cmd == 7:  # Calculate genre statistics
                        calc_genres(baseurl, userid)
                    else:
                        print("Invalid command. Please try again.")

        elif cmd == 2:  # Create Account
            if add_user(baseurl):
                print("Account creation successful. Please sign in.")
            else:
                print("Account creation failed. Please try again.")

        else:
            print("Invalid command. Please try again.")

main()
