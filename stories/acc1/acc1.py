from moviepy.editor import *
import moviepy.editor as mpy
import os
import math
from moviepy.config import change_settings
import random
from pathlib import Path

# Set the path for ImageMagick executable
change_settings({"IMAGEMAGICK_BINARY": r"D:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

# The folder containing background videos
BGVideosDirectory = r"D:\videos\stories\BGVideos"
# Folder where the original videos contained
originalVideosDirectory = r'D:\videos\stories\originalStoryVideos'
# Your "Follow me croma video" path
followVid = VideoFileClip(r"D:\videos\follow.mp4")
# like videos directory
likeVideos = r"D:\videos\likeVideos"
# Getting the original and background videos
videos = os.listdir(originalVideosDirectory)
BGvideos = os.listdir(BGVideosDirectory)
# Remove green background from the video
followVid = followVid.fx(mpy.vfx.mask_color, color=[21, 133, 0], thr=100, s=5)
followVid = followVid.set_start(random.randint(0, 7))   # start the  follow video at a random time 0-15
# Center the video in the middle
followVid = followVid.set_position(('center', 'center'))

tiktok_resolution = (1080, 1920)  # Width x Height
# Iterating through each video
for video in videos:
    # Getting a different background type for each video
    BGType = random.randint(0, len(BGvideos)-1)
    videoPath = rf"{BGVideosDirectory}\{BGvideos[BGType]}"
    BGVideos = os.listdir(videoPath)
    # keep reusing the background videos until they are the same duration as the Original video
    usedBGVideos = []
    BGVideoIndex = random.randint(0, len(BGVideos)-1)

    contentVideo = VideoFileClip(os.path.join(originalVideosDirectory, video))
    videoBG = VideoFileClip(videoPath+"/"+BGVideos[BGVideoIndex])
    videoBG = videoBG.subclip(3, videoBG.duration).set_start(0)
    videoBGDuration = videoBG.duration  # keeping track of the used videos
    usedBGVideos.append(BGVideoIndex)

    videoDuration = contentVideo.duration
    while True:
        if videoDuration >= videoBGDuration:  # loop until the BG video is longer than the original video
            while True:
                #  make sure we don't use the same BG video twice in a row
                if len(usedBGVideos) == len(BGVideos):
                    usedBGVideos = []
                BGVideoIndex = random.randint(0, len(BGVideos) - 1)
                if BGVideoIndex not in usedBGVideos:
                    usedBGVideos.append(BGVideoIndex)
                    break
            # add the next BG video to the end of the previous one
            newVideoBG = VideoFileClip(videoPath+"/"+BGVideos[BGVideoIndex])
            newVideoBG = newVideoBG.subclip(3, newVideoBG.duration).set_start(videoBGDuration)
            videoBGDuration += newVideoBG.duration
            videoBG = CompositeVideoClip([videoBG, newVideoBG])
        else:
            break
    videoBG.subclip(0, videoDuration)   # make the BG video and the original one the same duration

    contentVideo_audio = contentVideo.audio  # extract the audio from the content video
    # Give the BG video a TikTok ratio
    videoBG_resized = videoBG.resize(newsize=(tiktok_resolution[0], tiktok_resolution[1]))

    videoBG_resized = videoBG_resized.without_audio()  # Remove BG audio
    final_clip = videoBG_resized.set_audio(contentVideo_audio)  # set the extracted audio

    max_part_duration = 120  # 2 minutes in seconds

    # Calculate the number of parts
    parts = math.ceil(videoDuration / max_part_duration)

    partStart = 0  # set a counter for each clip to start from
    part = 1  # set a counter for parts

    # Define the directory path
    outputDirectory = Path(rf'D:\videos\stories\outputStories\{video[:-4]}')

    # Check if the directory exists and create it if it doesn't
    if not outputDirectory.exists():
        outputDirectory.mkdir(parents=True, exist_ok=True)
    while part <= parts:
        if part < 0:   # <-- change if the script got interrupted previously (it should be 0 by default)
            # ensure each part is not 2 minutes sharp
            partEnd = min(partStart + max_part_duration, videoDuration) - random.randint(-8, 8)
            partStart = partEnd - random.randint(4, 8)  # start with last 4-8 secs from the previous part
            partStart = max(0, partStart)  # Ensure partStart does not go negative

            part += 1
        else:
            # select a like video croma
            likeVid = fr"{likeVideos}\{os.listdir(likeVideos)[random.randint(0, len(os.listdir(likeVideos))-1)]}"
            likeVid = VideoFileClip(likeVid)
            likeVid = likeVid.fx(mpy.vfx.mask_color, color=[0, 213, 0], thr=100, s=5)
            likeVid = likeVid.set_start(random.randint(7, 15))
            # Center the video in the middle bottom
            likeVid = likeVid.set_position(('center', 'bottom'))

            partEnd = min(partStart + max_part_duration, videoDuration) - random.randint(-8, 8)

            partClip = (TextClip(f"part{part}",
                                 fontsize=100,
                                 stroke_color='black',
                                 stroke_width=5,
                                 color='white',
                                 font='Arial-Bold',
                                 method='caption',
                                 align='center',
                                 size=tiktok_resolution)
                        .set_duration(partEnd - partStart)
                        .set_position(('center', 'top')))  # overlay a part number in the center of each part

            titleClip = (TextClip(f"{video[:-4]}",
                                  fontsize=80,
                                  stroke_color='black',
                                  stroke_width=1,
                                  color='white',
                                  font='Cairo-Bold',
                                  method='caption',
                                  align='center',
                                  size=tiktok_resolution)
                         .set_duration(5)
                         .set_position(('center', -500)))   # overlay a title for the video

            final_part_clip = CompositeVideoClip([final_clip.subclip(partStart, partEnd),
                                                  partClip, titleClip, followVid, likeVid],
                                                 size=tiktok_resolution)

            final_part_clip.write_videofile(rf'{outputDirectory}\part_{part}.mp4',
                                            codec='libx264',
                                            fps=30,
                                            threads=4,
                                            preset='ultrafast')

            partStart = partEnd - random.randint(4, 8)
            partStart = max(0, partStart)

            part += 1
