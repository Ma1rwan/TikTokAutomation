import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx import resize, margin

# Path to the input video file
video_path = r"C:\Users\black\Downloads\Video\New folder\Fog Stock Footage _ No Copyright Drone Shots _ Royalty free drone shots _ free stock videos.mp4"
# Path to the output video file
output_path = r'final_tiktok_video.mp4'

# Load the video file
video = VideoFileClip(video_path).subclip(0, 10)

video.write_videofile(output_path, codec='libx264', audio_codec='aac')
