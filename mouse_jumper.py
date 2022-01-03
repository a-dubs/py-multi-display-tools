import pyautogui
from screeninfo import get_monitors
# from jsmin import jsmin
from time import sleep
# import json
# import pynput
from win32api import GetMonitorInfo, MonitorFromPoint
from win32gui import GetWindowRect, FindWindow
import ctypes
user32 = ctypes.windll.user32; 
user32.SetProcessDPIAware()
width, height= pyautogui.size()
print(width, height)
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# print(screensize,"\n\n\n")
monitors = get_monitors()

screen_info = {
    "screen"+str(i): {
        "width": (corners:=GetMonitorInfo(MonitorFromPoint((monitors[i].x + 100, monitors[i].y + 100)))["Work"])[2] - corners[0],
        "height": corners[3] - corners[1],
        "origin": corners[:2],
        "occ_w": 0.0,
        "occ_h": 0.0
    } 
    for i in range(len(get_monitors()))
}
print(screen_info)

count = 0
DISPLAYS = []
for m in monitors:
    print(m)
    d = {}
    d["x_off"] = m.x
    d["y_off"] = m.y
    d["width"] = m.width
    d["height"] = m.height
    d["name"] = m.name
    d["num"] = count
    d["center"] = (d["x_off"] + (0.5 * d["width"]), d["y_off"] + (0.5 * d["height"]))
    DISPLAYS.append(d)
    count+=1

print(DISPLAYS)

# for d in DISPLAYS:
#     print("Moving mouse to center of ", d["name"])
#     pyautogui.moveTo(*d["center"])
#     sleep(3);

def get_mouse_current_display(mouse_pos : tuple[int] = None):
    mx, my = None, None
    if mouse_pos:
        mx, my = mouse_pos[0], mouse_pos[1] 
    else:
        mx, my = pyautogui.position() 
    for d in DISPLAYS:
        if (d["x_off"] + d["width"] >= mx and mx >= d["x_off"]
        and d["y_off"] + d["height"] >= my and my >= d["y_off"] ):
            return d
    return None



# MOUSE_SCREEN_JUMP_MODE = "default"
# MOUSE_SCREEN_JUMP_MODE = "center"
MOUSE_SCREEN_JUMP_MODE = "dpi_scaled"

def mouse_on_border() -> tuple[bool , list[int]]:
    mx, my = pyautogui.position() 
    print(mx, my)
    d = get_mouse_current_display()
    border_dir_result = [0,0]
    border_dir_result[0] =  (int(mx == d["x_off"]) * -1) + (int(mx == (d["x_off"] + d["width"] - 1)) * 1)
    border_dir_result[1] =  (int(my == d["y_off"]) * -1) + (int(my == (d["y_off"] + d["height"] - 1)) * 1)

    return (border_dir_result[0] + border_dir_result[1]) != 0, border_dir_result 

def jump_mouse_across_border():
    if MOUSE_SCREEN_JUMP_MODE == "dpi_scaled":
        mob, mobd = mouse_on_border()
        if mob:
            mx, my = pyautogui.position()
            test_mouse_pos = ((mx+(mobd[0]*100)) , (my+(mobd[1]*100)))
            if (new_display := get_mouse_current_display(test_mouse_pos)):
                print("jumped mouse across border to", new_display["name"])
                pyautogui.moveTo(*new_display["center"])
            else:
                print("no screen on this edge to jump to")



# number of display mouse was on last
mcd_last = -1
mob_last = -1
while True:
    print(pyautogui.position())
    mob = mouse_on_border()[0]
    # print("mouse is on border =", mob)
    mcd = get_mouse_current_display()
    if mob != mob_last:
        mob_last = mob
        if mob:
            print("Mouse on border!")
    # mouse has moved to new screen
    if mcd and mcd["num"] != mcd_last:
        print("mouse is now on display: " + mcd["name"])
        mcd_last = mcd["num"]
    #     pyautogui.moveTo(*mcd["center"])
    jump_mouse_across_border()
    sleep(0.5)


