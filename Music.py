import time
import os
from os import chdir as cd
import pywinauto
from pywinauto.application import Application
from pywinauto import Desktop
import pyautogui
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

#############################################################################

PlaylistsWhiteSpace = (120, 1100)
FirstPlaylist = (120, 550)
PlaylistIncrement = 72

SecondPlaylist = (120, 585)
PhonePlaylist = (120, 425)
PhoneCloseTab = (15, 425)
LaptopSongsTab = (120, 310)
PlaylistWhiteSpace = (1080, 365)

PhoneIcon = (330, 120)
SyncButton = (1630, 1090)

FilePath = (975, 175)
FileName = (1075, 720)
FileWhiteSpace = (755, 335)
FirstFilePosition = (910, 330)
OutsideFilePosition = (1700, 330)

MusicDirectory = "C:\\Users\\harsh\\Music"

#############################################################################

TopHitsPlaylist = {
    "name": "Todays_Top_Hits",
    "link": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",
    "file": MusicDirectory + "\\SpotDL" + "\\TodaysTopHits"
    }

Daily1 = {
    "name": "Daily1",
    "link": "https://open.spotify.com/playlist/37i9dQZF1E38vsyxKYsDLS",
    "file": MusicDirectory + "\\SpotDL" + "\\Daily1"
    }

Daily2 = {
    "name": "Daily2",
    "link": "https://open.spotify.com/playlist/37i9dQZF1E38EeyepmlG68",
    "file": MusicDirectory + "\\SpotDL" + "\\Daily2"
    }

Daily3 = {
    "name": "Daily3",
    "link": "https://open.spotify.com/playlist/37i9dQZF1E39tu7wQTUyTw",
    "file": MusicDirectory + "\\SpotDL" + "\\Daily3"
    }

Telugu = {
    "name": "Telugu",
    "link": "https://open.spotify.com/playlist/489ypmPBNS5F28kGgOUcnu",
    "file": MusicDirectory + "\\SpotDL" + "\\Telugu"
    }

Bruh = {
    "name": "MyBruh",
    "link": "https://open.spotify.com/playlist/3pM6opHN1PQzkMsThcjojP",
    "file": MusicDirectory + "\\SpotDL" + "\\MyBruh"
    }

InternetRewind = {
    "name": "InternetRewind",
    "link": "https://open.spotify.com/playlist/37i9dQZF1DWSPMbB1kcXmo",
    "file": MusicDirectory + "\\SpotDL" + "\\InternetRewind"
    }

AllPlaylists = [TopHitsPlaylist, Daily1, Telugu, Bruh]
AllPlaylists = sorted(AllPlaylists, key=lambda i: i['name'])
#############################################################################

if os.path.exists(MusicDirectory + "\\SpotDL"):
    pass
else:
    os.system("mkdir " + MusicDirectory + "\\SpotDL")

for playlist in AllPlaylists:
    if os.path.exists(playlist['link']):
        pass
    else:
        os.system("mkdir " + playlist["file"])
        cd(playlist["file"])
        sync_file = playlist['name'] + ".sync.spotdl"
        os.system(f"spotdl sync {playlist['link']} --save-file {sync_file}")

for playlist in AllPlaylists:
    cd(playlist["file"])
    os.system(f"spotdl sync '{playlist['name']}.sync.spotdl'")

AllWindows = pywinauto.findwindows.find_windows(title_re='iTunes')
Handle = AllWindows[len(AllWindows)-1]
App = Application().connect(title='iTunes', found_index=0, timeout=10)
app_dialog = App.window(title_re='iTunes', found_index=0, handle=Handle)

if app_dialog.exists():
    app_dialog.set_focus()


def remove_existing_playlists():
    for playlist in AllPlaylists:
        pyautogui.moveTo(FirstPlaylist)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.press('delete')
        time.sleep(0.25)
def create_all_playlists():
    for playlist in AllPlaylists:
        pyautogui.moveTo(PlaylistsWhiteSpace)
        pyautogui.click()
        time.sleep(0.1)

        pyautogui.keyDown('ctrl')
        pyautogui.press('n')
        pyautogui.keyUp('ctrl')

        pyautogui.write(playlist['name'])
        time.sleep(0.1)
    pyautogui.moveTo(PlaylistsWhiteSpace)
    pyautogui.click()
    time.sleep(0.1)
def fill_all_playlists():
    playlistcount = 0

    for playlist in AllPlaylists:

        # Open Playlist
        pyautogui.moveTo(FirstPlaylist + (0, PlaylistIncrement * playlistcount))
        pyautogui.click()
        time.sleep(0.25)

        pyautogui.moveTo(PlaylistWhiteSpace)
        pyautogui.click()
        time.sleep(0.1)

        # Open File Explorer
        pyautogui.keyDown('ctrl')
        pyautogui.press('o')
        pyautogui.keyUp('ctrl')

        time.sleep(0.5)

        pyautogui.moveTo(FilePath)
        pyautogui.click()
        pyautogui.write(playlist['file'])
        time.sleep(0.25)

        pyautogui.press('enter')

        pyautogui.moveTo(FileWhiteSpace)
        pyautogui.click()
        time.sleep(0.1)

        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

        time.sleep(0.25)

        pyautogui.moveTo(FirstFilePosition)
        pyautogui.dragTo(1700, 500, 0.4, button='left')

        # Enter
        pyautogui.press('enter')
        playlistcount += 1
        time.sleep(1.5)
def put_playlists_in_phone():
    playlistcount = 0

    for playlist in AllPlaylists:
        pyautogui.moveTo(FirstPlaylist + (0, PlaylistIncrement * playlistcount))
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.5)

        pyautogui.dragTo(120, 422, 0.4, button='left')
        time.sleep(2)
        playlistcount += 1
def sync_to_phone():
    pyautogui.moveTo(PhoneIcon)
    pyautogui.click()
    time.sleep(0.1)

    pyautogui.moveTo(SyncButton)
    pyautogui.click()


# remove_existing_playlists()
# create_all_playlists()
# fill_all_playlists()
# put_playlists_in_phone()
# sync_to_phone()
