import yt_dlp

# Specify the YouTube video URL
video_url = 'https://www.youtube.com/watch?v=4TBjzYaKx6I'

# Create an instance of yt-dlp
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',  # Download the best quality video and audio
    'outtmpl': r'C:\Users\black\Downloads\video_filename.%(ext)s',  # Output file template
}

# Download the video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])


import yt_dlp

# Specify the YouTube playlist URL
playlist_url = 'https://www.youtube.com/playlist?list=PLWSOb5qekkMXhXaD9iJs_zx7Y_CEbd2ul'

# Create an instance of yt-dlp
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',  # Download the best quality video and audio
    'outtmpl': r'C:\Users\black\Downloads\%(title)s.%(ext)s',  # Output file template
    'noplaylist': False,  # Download all videos in the playlist
}

# Download all videos in the playlist
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])
