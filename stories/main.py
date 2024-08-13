from moviepy.editor import *
import moviepy.editor as mpy
import os
import numpy as np
import math
from moviepy.config import change_settings
import random
change_settings({"IMAGEMAGICK_BINARY": r"D:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

# Load the background and content videos
BGVideosDirectory = r"D:\videos\stories"
originalVideosDirectory = r'D:\videos\stories\originalStoryVideos'
followVid = VideoFileClip(r"D:\videos\follow.mp4")

videos = os.listdir(originalVideosDirectory)

followVid = followVid.fx(mpy.vfx.mask_color, color=[21, 133, 0], thr=100, s=5)
followVid = followVid.set_position(('center', 'center'))
tiktok_resolution = (1080, 1920)  # Width x Height
videoPath = r"\BGRugsVideos"
for video in videos:
    BGType = random.randint(0, 2)
    # if BGType == 0:
    #     videoPath = r"\BGGTAVideos"
    #     pass
    if BGType == 0 or BGType == 1:
        videoPath = r"\BGRugsVideos"
        print("using BGRugsVideos")
    elif BGType == 2:
        videoPath = r"\BGTruckVideos"
        print("using BGTruckVideos")
    BGVideos = os.listdir(BGVideosDirectory+videoPath+"\\" )
    usedBGVideos = []
    BGVideoIndex = random.randint(0,len(BGVideos)-1)
    contentVideo = VideoFileClip(os.path.join(originalVideosDirectory, video))
    videoBG = VideoFileClip(BGVideosDirectory+videoPath+"/"+BGVideos[BGVideoIndex])
    videoBGDuration = videoBG.duration
    usedBGVideos.append(BGVideoIndex)

    videoDuration = contentVideo.duration
    while True:
        if videoDuration > videoBGDuration:
            while True:
                if len(usedBGVideos) == len(BGVideos):
                    usedBGVideos = []
                BGVideoIndex = random.randint(0, len(BGVideos) - 1)
                if BGVideoIndex not in usedBGVideos:
                    usedBGVideos.append(BGVideoIndex)
                    break
            newVideoBG = VideoFileClip(BGVideosDirectory+videoPath+"/"+BGVideos[BGVideoIndex]).set_start(videoBGDuration)
            videoBGDuration += newVideoBG.duration
            videoBG = CompositeVideoClip([videoBG, newVideoBG])
        else:
            break
    videoBG.subclip(0, videoDuration)

    # Resize the background video to fit the bottom half of the screen
    contentVideo_audio = contentVideo.audio
    videoBG_resized = videoBG.resize(newsize=(tiktok_resolution[0], tiktok_resolution[1]))
    followVid = followVid.set_position('center')

    # Convert all clips to RGB
    videoBG_resized = videoBG_resized.without_audio()
    videoBG_resized = videoBG_resized.set_audio(contentVideo_audio)

    # Create the final composite video
    # final_clip = CompositeVideoClip([videoBG_resized, contentVideo_resized], size=tiktok_resolution)
    final_clip = videoBG_resized
    max_clip_duration = 120  # 2 minutes in seconds

    # Calculate the number of parts
    parts = math.ceil(videoDuration / max_clip_duration)

    clipStart = 0
    part = 1
    from pathlib import Path

    # Define the directory path
    directory = Path(rf'D:\videos\stories\outputStories\{video[:-4]}')

    # Check if the directory exists and create it if it doesn't
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
    while part <= parts:
        if part < 0:
            clipEnd = min(clipStart + max_clip_duration, videoDuration)
            clipStart = clipEnd - random.randint(4, 8)
            clipStart = max(0, clipStart)  # Ensure clipStart does not go negative

            part += 1
        else:

            clipEnd = min(clipStart + max_clip_duration, videoDuration)

            partClip = TextClip(f"part{part}", fontsize=100, stroke_color='black', stroke_width=5, color='white',
                                font='Arial-Bold', method='caption', align='center', size=tiktok_resolution).set_duration(
                clipEnd - clipStart).set_position(('center', 'top'))

            titleClip = TextClip(f"{video[:-4]}", fontsize=80, stroke_color='black', stroke_width=1, color='white',
                                font='Calibri-Bold', method='caption', align='center', size=tiktok_resolution).set_duration(5).set_position(
                ('center', -500))

            final_part_clip = CompositeVideoClip([final_clip.subclip(clipStart, clipEnd), partClip, titleClip, followVid], size=tiktok_resolution)
            final_part_clip.write_videofile(rf'D:\videos\stories\outputStories\{video[:-4]}\part_{part}.mp4',
                                            codec='libx264', fps=30, threads=4, preset='ultrafast')

            clipStart = clipEnd - random.randint(4, 8)
            clipStart = max(0, clipStart)  # Ensure clipStart does not go negative

            part += 1
