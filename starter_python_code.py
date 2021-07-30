import ctypes
import pygetwindow
import pyautogui
from screeninfo import get_monitors
from jsmin import jsmin
from time import sleep
import json
from win32api import GetMonitorInfo, MonitorFromPoint
from win32gui import GetWindowRect, FindWindow

CONFIG_FILENAME = "user_config.json"

json_str = ""
with open(CONFIG_FILENAME) as js_file:
    json_str = jsmin(js_file.read())

config = json.loads(json_str)
profile = config["profile"]
screen_names = config["screen_names"]
targets = []

monitors = get_monitors()

for target in profile:
    targets.append(target)
    if profile[target].get("width"):
        profile[target]["width"] = eval(profile[target]["width"])
    else:
        profile[target]["width"] = 1
    if profile[target].get("height"):
        profile[target]["height"] = eval(profile[target]["height"])
    else:
        profile[target]["height"] = 1
screens = {
    screen_names[i]: {
        "width": (corners:=GetMonitorInfo(MonitorFromPoint((monitors[i].x + 100, monitors[i].y + 100)))["Work"])[2] - corners[0],
        "height": corners[3] - corners[1],
        "origin": corners[:2],
        "occ_w": 0.0,
        "occ_h": 0.0
    } 
    for i in range(len(screen_names))
}

for target in targets:
    wins = pygetwindow.getWindowsWithTitle(target)
    if target == "spotify" and not wins:
        pyautogui.press("playpause")
        while not (wins:=pygetwindow.getWindowsWithTitle("spotify")):
            sleep(.01)
        pyautogui.press("playpause")

    if wins:
        for win in wins: 
            screen = screens[profile[target]["screen"]]
                            
            win.restore()
            win.restore()
            
            #print(GetWindowRect(FindWindow(None, win.title)))

            new_w = (int) (screen["width"] * (occ_w:=profile[target]["width"])) 
            new_h = (int) (screen["height"] * (occ_h:=profile[target]["height"]))
            win.resizeTo(new_w, new_h)

            new_x = screen["origin"][0]
            if screen["occ_w"] + occ_w <= 1.0:
                new_x += (int) (screen["width"] * screen["occ_w"]) 
            
            new_y = screen["origin"][1]
            if new_x == screen["origin"][0] and screen["occ_h"] + occ_h <= 1.0:
                new_y += (int) (screen["height"] * screen["occ_h"])
            screen["occ_w"] = min(1, screen["occ_w"] + occ_w)
            screen["occ_h"] = min(1, screen["occ_h"] + occ_h)
            win.moveTo(new_x, new_y)
            print(target, '\n', win)
            #print(profile[target]["screen"], '\n', screen)

"""
print("spotify: \n", pygetwindow.getWindowsWithTitle('spotify')[0])
print("discord: \n", pygetwindow.getWindowsWithTitle('discord')[0])
print("steam: \n", pygetwindow.getWindowsWithTitle('steam')[0])
"""

