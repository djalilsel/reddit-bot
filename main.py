import numpy as np 
from getPosts import getPosts, extractComments, limitComments, getVoice, getScreenshot, getVideo, getBg, createThumbnail
from selenium import webdriver
from moviepy.editor import concatenate_videoclips, CompositeVideoClip
import pyttsx3
import os


print("start")

#arr = np.array(["1c0s4ub", "1c0s7xg"])
driver = webdriver.Chrome()
driver.maximize_window()

arr = np.load('id.npy')

posts = getPosts()

for post in posts:
    if post.id in arr:
        print("arr contains 'id'")
    else:
        postObject = extractComments(post)
        postObject["comment"] = limitComments(postObject["comment"])

        arr = np.append(arr, postObject["id"])

        commentsplustitle = postObject["comment"].copy()
        commentsplustitle.append({
                "id": post.id,
                "score": 9999,
                "body": post.title,
                "permalink": post.url
            })
        
        voiceOvers = getVoice(postObject["id"], commentsplustitle)
        
        screenshots = getScreenshot(driver, postObject["url"], postObject["id"], postObject["comment"])

        clips = []
        for i, screen in enumerate(screenshots):
            clip = getVideo(screen, voiceOvers[i])
            clips.append(clip)
        titleAndComments = concatenate_videoclips(clips, method="compose")
        if titleAndComments.duration > 58:
            titleAndComments.set_duration(58)
        bg = getBg()
        finalVideo = CompositeVideoClip(clips=[bg.set_position(("center", "center")), titleAndComments.set_position(("center", "center"))], size=(1070, 1920)).set_duration(58)
        
        outputFile = f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/video/post-{postObject['id']}.mp4"
        outputTitle = f"C:/Users/djali/OneDrive/Desktop/python/reddit-bot/titles/post-{postObject['id']}.txt"
        with open(outputTitle, "w") as f:
            f.write(postObject["title"])
        finalVideo.write_videofile(outputFile, codec="mpeg4", threads= 12, bitrate= "8000k", fps= 24)
        createThumbnail(postObject["id"], postObject["title"])


driver.quit()

np.save('id.npy', arr)

print("end")



