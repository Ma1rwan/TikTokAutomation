from moviepy.editor import TextClip
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"D:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

print(TextClip.list("font"))
