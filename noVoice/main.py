import os
from moviepy.config import change_settings
from moviepy.editor import *
from PIL import Image, ImageDraw
import numpy as np
import random
import re

# Change settings for ImageMagick
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def create_rounded_rectangle(size, radius, color):
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, size[0], size[1]], radius, fill=color)
    return img

def sanitize_filename(value):
    # Remove invalid characters for a file name
    return re.sub(r'[:<>|\\/*?"]', '', value)

facts = open("facts.csv", "r", encoding="utf-8").readlines()
for index, line in enumerate(facts):
    if index == 0:
        continue

    parts = line.split("|")
    Topic = parts[0].upper()
    Fact = parts[1]
    Title1 = parts[2]
    Part1 = parts[3]
    Title2 = parts[4]
    Part2 = parts[5]
    Title3 = parts[6]
    Part3 = parts[7]
    Title4 = parts[8]
    Part4 = parts[9]
    Title5 = parts[10]
    Part5 = parts[11]
    Title6 = parts[12]
    Part6 = parts[13]
    Title7 = parts[14]
    Part7 = parts[15]
    Title8 = parts[16]
    Part8 = parts[17]
    Title9 = parts[18]
    Part9 = parts[19]
    Title10 = parts[20]
    Part10 = parts[21]

    # Load the video file
    videos = [f for f in os.listdir(r"D:\videos\noVoice\videos")]
    video_file = videos[random.randint(0, len(videos) - 1)]
    video = VideoFileClip(r"D:\videos\noVoice\videos/" + video_file)

    audios = [f for f in os.listdir(r"D:\videos\noVoice\audios")]
    audio_file = audios[random.randint(0, len(audios) - 1)]
    audio = AudioFileClip(r"D:\videos\noVoice\audios/" + audio_file)
    # Select a random start time ensuring it fits within the video duration
    max_start_time = video.duration - 70  # Assuming the video should be at least 70 seconds long
    if max_start_time > 0:
        start_time = random.uniform(0, max_start_time)
    else:
        start_time = 0
    video = video.subclip(start_time, video.duration)
    # video = video.subclip(start_time, start_time + min(20, video.duration - start_time))

    # Create TextClips
    topicClip = TextClip(Topic, fontsize=70, color='white', font='Arial-Bold', method='caption', align='center')
    factClip = TextClip(Fact, fontsize=100, stroke_color='black', stroke_width=3, color='white', font='Lobster-Bold', method='caption', align='center', size=video.size)

    # Create a rounded rectangle background for the topic text
    bg_size = (topicClip.w + 50, topicClip.h + 50)
    rounded_rect = create_rounded_rectangle(bg_size, 25, (0, 0, 0, 153))  # Semi-transparent black

    # Convert the rounded rectangle to a MoviePy clip
    bg_array = np.array(rounded_rect)
    background = ImageClip(bg_array).set_duration(video.duration)

    # Position the background and text
    topicClip = CompositeVideoClip([background.set_position('center'), topicClip.set_position('center')])
    partsTimePlace = 0
    topicClip = topicClip.set_duration(video.duration)
    partsDuration = random.randint(6, 7)
    factClip = factClip.set_position(("center", 0.5)).set_start(0).set_end(partsDuration)
    partsTimePlace += partsDuration

    # Create other text clips
    jendix = 2
    text_clips = [topicClip.set_position(("center", 100)), factClip]

    while jendix < 20:
        partsDuration = random.randint(4, 6)
        title = TextClip(parts[jendix], fontsize=100, stroke_color='black', stroke_width=5, color='white', font='Arial-Bold', method='caption', align='center', size=video.size)
        part = TextClip(parts[jendix + 1], fontsize=70, stroke_color='black', stroke_width=5, color='white', font='Arial-Bold', method='caption', align='center', size=video.size)

        # Set durations and positions
        title = title.set_position(("center", -300)).set_start(partsTimePlace).set_end(partsTimePlace + partsDuration)
        part = part.set_position(("center", 200)).set_start(partsTimePlace).set_end(partsTimePlace + partsDuration)
        text_clips.extend([title, part])
        partsTimePlace += partsDuration

        jendix += 2
    finalVideo = video.without_audio()

    finalVideo = finalVideo.subclip(0, partsTimePlace)
    finalVideo = finalVideo.set_audio(audio)
    # Overlay text on the video
    final_video = CompositeVideoClip([finalVideo] + text_clips).subclip(0, partsTimePlace)
    # Sanitize Fact for file name
    sanitized_fact = sanitize_filename(Fact.strip('"'))

    # Save the result
    final_video.write_videofile(
        fr"D:\videos\noVoice\outputVideos\#fact {sanitized_fact} #facts #girls #girlsfact #boysfact #sigmamale #sigma #Love #viral #dailyfacts.mp4",
        codec="libx264",
        audio_codec='aac',
        fps=30,
        threads=4
    )
