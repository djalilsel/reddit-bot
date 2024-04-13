from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil
import pyautogui
import keyboard

while True:
    videos = os.listdir(r"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/video/not good")
    titles = os.listdir(r"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/titles/")
    thumbnails = os.listdir(r"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/thumbnails/")
    videos = [video for video in videos if video.endswith(".mp4")]
    if len(videos) != 0:
        for video in videos:
            if video[:-4] + ".txt" not in titles or f"thumbnail-{video[5:-4]}.png" not in thumbnails:
                print(f"Missing {video}")
                time.sleep(10)
                continue
            titleFile = [title for title in titles if title.startswith(video[:-4])][0]
            with open(f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/titles/{titleFile}", "r") as f:
                titleText = f.read()
            titleText = titleText[:70]
            time.sleep(5)
            pyautogui.click(1000, 500)
            time.sleep(2)
            keyboard.write(fr"C:\Users\djali\OneDrive\Desktop\python\reddit-bot\video\not good\{video}")
            # keyboard.write(fr"C:\Users\djali\Videos\2024-04-12 03-55-58.mp4")
            keyboard.press_and_release('enter')
            time.sleep(1)
            pyautogui.click(600, 330)
            keyboard.write(titleText)
            time.sleep(5)
            pyautogui.scroll(-3000)
            time.sleep(5)
            pyautogui.click(750, 625)
            while not pyautogui.pixelMatchesColor(790, 790, (254, 44, 85)):
                pass
            pyautogui.click(790, 790)
            while not pyautogui.pixelMatchesColor(950, 600, (254, 44, 85)):
               pass
            pyautogui.click(950, 600)
            shutil.move(f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/video/not good/{video}", f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/uploaded/videos/{video}")
            shutil.move(f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/titles/{video[:-4]}.txt", f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/uploaded/titles/{video[:-4]}.txt")
            print(f"Uploaded {video}")
            time.sleep(5)
            keyboard.press('ctrl')
            keyboard.press_and_release('r')
            keyboard.release('ctrl')
    else:
        print("No videos to upload")
        time.sleep(10)



