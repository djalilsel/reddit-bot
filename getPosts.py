import moviepy.editor
import moviepy.video
import moviepy.video.VideoClip
import praw

from gtts import gTTS
import pyttsx3


import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import cv2
import numpy as np
from matplotlib import pyplot as plt

from moviepy.editor import ImageClip, AudioClip, VideoFileClip, AudioFileClip, CompositeVideoClip
import moviepy
import random

from PIL import Image, ImageDraw
from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageDraw, ImageFont

import time


def getPosts ():
    reddit = praw.Reddit(
        client_id='cuJshn31uyED2PlbXidbhg',
        client_secret='bU_AA3p2f0mA1see_91sJpx9N091BA',
        user_agent='windows:djalti-bot:v1.0 (by u/Djalti)',
    )
    posts = reddit.subreddit("AskReddit").hot( limit=5 )
    posts = [post for post in posts if not post.over_18]
    posts = [post for post in posts if not len(post.comments.list()) < 20]
    return posts

def extractComments (post):

    postObject = {
        "id": post.id,
        "title": post.title,
        "url":  post.url,
        "comment": []
    }
    
    post.comments.replace_more(limit=1)
    for comment in post.comments.list():
        postObject["comment"].append({
            "id": comment.id,
            "score": comment.score,
            "body": comment.body,
            "permalink": comment.permalink,
            "parent_id": comment.parent_id
        })
    return postObject

def limitComments (comments):
    updated = []
    comments.sort(key=lambda x: x["score"], reverse=True)
    for comment in comments:
        if len(comment["body"]) < 200 and len(comment["body"]) > 100 and len(comment["body"]) > 1 and comment["body"] != "[deleted]" and comment["body"] != "[removed]" and comment["body"] != " " and len(updated) <= 8 and comment["parent_id"].startswith("t1_"): 
            updated.append(comment)
    return updated

def getVoice (postId, comments):
    comments.insert(0, comments.pop())
    filename = f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/voice/post-{postId}"
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+15)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    voiceOvers = []
    os.makedirs(filename, exist_ok=True)
    for comment in comments:
        filePath = f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/voice/post-{postId}/comment-{comment['id']}.mp3"
        engine.save_to_file(comment['body'], filePath)
        engine.runAndWait()
        # gTTS(text=comment['body'], lang='en', tld='us', slow=False, lang_check=False).save(filePath)
        voiceOvers.append(filePath)
    return voiceOvers

def getScreenshot(driver, url, postId, comments):
    screenshots = []
    fileName = f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/screenshot/post-{postId}"
    
    driver.get(url)

    os.makedirs(fileName, exist_ok=True)
    postScreenshot = f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/screenshot/post-{postId}/post-{postId}.png"

    element = driver.find_element(By.ID, f"t3_{postId}")
    element.screenshot(postScreenshot)
    screen = cv2.imread(postScreenshot)
    cv2.imwrite(postScreenshot, screen)
    screenshots.append(postScreenshot)

    for comment in comments:
        print("forwarding to " + comment["permalink"])
        driver.get(f"https://www.reddit.com{comment["permalink"]}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[thingid='t1_{comment['id']}']")))
        driver.execute_script("document.getElementById('-post-rtjson-content').style.fontSize = '20px';")
        driver.execute_script("document.getElementById('-post-rtjson-content').style.lineHeight = '1.5';")


        elem = driver.find_elements(By.CSS_SELECTOR, f"[thingid='t1_{comment['id']}']")
        posTop = elem[1].location["y"]
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, f"t1_{comment['id']}-comment-rtjson-content")))
        text = driver.find_element(By.ID, f"t1_{comment['id']}-comment-rtjson-content")
        h = text.size["height"]
        posBottom = text.location["y"] + h + 30
        hight = posBottom - posTop
        screenshotName = f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/screenshot/post-{postId}/comment-{comment['id']}.png"
        elem[1].screenshot(screenshotName)

        screen = cv2.imread(screenshotName)
        screen = screen[0:hight, 0:1920]
        cv2.imwrite(screenshotName, screen)
        screen = cv2.imread(screenshotName)
        cv2.imwrite(screenshotName, screen)
        
        screenshots.append(screenshotName)
    return screenshots

def getVideo (screenshotFile, voiceOverFile):
    print(screenshotFile, voiceOverFile)
    imageClip = ImageClip(screenshotFile)
    (w, h) = imageClip.size
    audioClip = AudioFileClip(voiceOverFile)
    if audioClip.duration > 59:
        audioClip = audioClip.subclip(0, 59)
        videoClip = (imageClip.set_audio(audioClip)
                            .set_duration(59))
    else:
        videoClip = (imageClip.set_audio(audioClip)
                            .set_duration(audioClip.duration))
    return videoClip

def getBg ():
   randomIndex = random.randint(1, 5)
   bgName = f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/bg/mincraft{randomIndex}.mp4"
   bg = VideoFileClip(filename=bgName)
   bg.set_duration(59)
   return bg

def createThumbnail(postId, title):
    randomIndex = random.randint(1, 8)
    bgName = f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/thumb-bg/thumbnail{randomIndex}.PNG"
    image = Image.open(bgName)
    image = image.resize((1080, 1920))
    draw = ImageDraw.Draw(image)
    rect_position = (100, (image.height - 500) // 2)
    rect_size = (rect_position[0] + 880, rect_position[1] + 500)
    draw.rectangle([rect_position, rect_size], fill=(0, 255, 255), outline=(0, 0, 0), width=10)
    max_text_width = rect_size[0] - 2 * rect_position[0]
    font_size = 60
    words = title.split()
    new_title = '\n'.join([' '.join(words[i:i+5]) for i in range(0, len(words), 5)])
    font = ImageFont.truetype("arial.ttf", font_size)
    
    text_position = ((image.width - 820) // 2, (image.height - 200) // 2)
    draw.multiline_text(text_position, new_title, fill='white', stroke_width=4, stroke_fill='black', font=font, align='center')
    
    image.save(f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/thumbnails/thumbnail-{postId}.png")
    return bgName



