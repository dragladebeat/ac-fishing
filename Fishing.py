import cv2
import numpy as np
import pyautogui
import time
import asyncio
import wx
import sys
from pynput.keyboard import Key, Controller, Listener
from pynput.mouse import Button, Controller



method = cv2.TM_SQDIFF_NORMED
# method = cv2.TM_CCOEFF
# Read the images from the file
image_hook = cv2.imread('hook.png')
image_fish = cv2.imread('fish.png')
# Cast in progress
# image_cast = cv2.imread('cast.png')

# Get the size of the template. This is the same size as the match.

app = wx.App(False)
width, height = wx.GetDisplaySize()

i = 0
x = width / 2 - (width / 19.5 / 2)
y = height / 9.3
fishingRegWidth = width / 19.5
fishingRegHeight = height / 1.3


keyboard = Controller()

mouse = Controller()

async def pressKey(duration) :
    # keyboard.press(Key.space)
    # await asyncio.sleep(duration)
    # keyboard.release
    mouse.position = (1649,852)
    mouse.press(Button.left)
    await asyncio.sleep(duration)
    mouse.release

async def generateImage() :
    cv2.rectangle(large_image, (MPxHook,MPyHook),(MPxHook+tcolsHook,MPyHook+trowsHook),(0,0,255),2)
    cv2.rectangle(large_image, (MPxFish,MPyFish),(MPxFish+tcolsFish,MPyFish+trowsFish),(0,0,255),2)

    filename = "output/proses-"
    filename += str(i)
    filename += ".png"
    cv2.imwrite(filename, large_image)

while(True) :
    start_time = time.time()
    i+=1
    large_image = pyautogui.screenshot(region=(x,y,fishingRegWidth, fishingRegHeight))
    large_image = cv2.cvtColor(np.array(large_image), cv2.COLOR_RGB2BGR)

    # while True : 
    #     large_image = pyautogui.screenshot()
    #     large_image = cv2.cvtColor(np.array(large_image), cv2.COLOR_RGB2BGR)
    #     cv2.imshow('output', large_image)
    #     cv2.waitKey(0)
    #     time.sleep(2)

    # print(large_image)

    result_hook = cv2.matchTemplate(image_hook, large_image, method)
    result_fish = cv2.matchTemplate(image_fish, large_image, method)

    # # We want the minimum squared difference
    mnHook,_,mnLocHook,_ = cv2.minMaxLoc(result_hook)
    mnFish,_,mnLocFish,_ = cv2.minMaxLoc(result_fish)

    # # Draw the rectangle:
    # # Extract the coordinates of our best match
    MPxHook,MPyHook = mnLocHook
    MPxFish,MPyFish = mnLocFish

    trowsHook,tcolsHook = image_hook.shape[:2]
    trowsFish,tcolsFish = image_fish.shape[:2]
    # trowsCast,tcolsCast = image_cast.shape[:2]

    y1Hook = MPyHook
    y2Hook = y1Hook + tcolsHook
    y1Fish = MPyFish
    y2Fish = MPyFish + tcolsFish

    print("Hook: ", MPxHook, " ", MPyHook, " ", trowsHook, " ", tcolsHook)
    print("Fish", MPxFish, " ", MPyFish, " ", trowsFish, " ", tcolsFish)

    if y1Fish <= y1Hook :
        print("Fish is on top of hook")
        # Ceritanya pencet space
        asyncio.run(pressKey(0.3))
    elif y2Fish <= y2Hook and y1Fish > y1Hook:
        print("Fish is in bound")
        asyncio.run(pressKey(0.1))
        # Ceritanya diem
    elif y1Fish > y2Hook : 
        print("Fish is under hook")
        # keyboard.release(Key.space)
        mouse.release(Button.left)
        # Ceritanya diem
    else :
        print("Condition Unknown")

    


# # Step 3: Draw the rectangle on large_image

    # asyncio.run(generateImage())

    # asyncio.run(checkFishingState())

    print("--- %s seconds ---" % (time.time() - start_time))

# # Display the original image with the rectangle around the match.
# cv2.imshow('output',large_image)

# # The image is only displayed if we call this
# cv2.waitKey(0)