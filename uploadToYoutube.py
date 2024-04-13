from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\djali\AppData\Local\Google\Chrome\User Data")
options.add_argument(r'--profile-directory=Profile 3')
service = webdriver.ChromeService(executable_path=r"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/depends/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
while True:
    videos = os.listdir(r"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/video/")
    titles = os.listdir(r"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/titles/")
    thumbnails = os.listdir(r"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/thumbnails/")
    videos = [video for video in videos if video.endswith(".mp4")]
    if len(videos) != 0:
        for video in videos:
            print(video)
            if video[:-4] + ".txt" not in titles or f"thumbnail-{video[5:-4]}.png" not in thumbnails:
                print(f"Missing {video}")
                time.sleep(10)
                continue
            titleFile = [title for title in titles if title.startswith(video[:-4])][0]
            with open(f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/titles/{titleFile}", "r") as f:
                titleText = f.read()
            titleText = titleText[:70]
            driver.get('https://studio.youtube.com/channel/UCTUPThqT0PqHwDJanYqWdXQ/videos/upload')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "create-icon")))
            driver.find_element(By.ID, "create-icon").click()
            driver.find_element(By.ID, "text-item-0").click()
            driver.find_element(By.NAME, "Filedata").send_keys(f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/video/{video}")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Add a title that describes your video (type @ to mention a channel)']")))
            title = driver.find_element(By.XPATH, "//div[@aria-label='Add a title that describes your video (type @ to mention a channel)']")
            description = driver.find_element(By.XPATH, "//div[@aria-label='Tell viewers about your video (type @ to mention a channel)']")
            title.clear()
            description.clear()
            title.send_keys(f"{titleText} #askreddit #shorts #reddit")
            description.send_keys("#askreddit #shorts #reddit")
            #thumbnail = driver.find_element(By.ID, "file-loader").send_keys(f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/thumbnails/thumbnail-{video[5:-4]}.png")
            radioBtn = driver.find_elements(By.ID, "radioContainer")
            radioBtn[0].click()
            nextBtn = driver.find_element(By.ID, "next-button").click()
            nextBtn = driver.find_element(By.ID, "next-button").click()
            nextBtn = driver.find_element(By.ID, "next-button").click()
            radioBtn = driver.find_elements(By.ID, "radioContainer")
            radioBtn[2].click()
            WebDriverWait(driver, float('inf')).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "progress-label"), "Checks complete. No issues found."))
            nextBtn = driver.find_element(By.ID, "done-button").click()
            shutil.move(f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/video/{video}", f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/uploaded/videos/{video}")
            shutil.move(f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/titles/{video[:-4]}.txt", f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/uploaded/titles/{video[:-4]}.txt")
            print(f"Uploaded {video}")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "close-button")))
    else:
        print("No videos to upload")
        time.sleep(10)

