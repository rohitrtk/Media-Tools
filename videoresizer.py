import os

import moviepy.editor as mp

# Default width and height
DEFAULT_WIDTH   = 640
DEFAULT_HEIGHT  = 360

# Video types that can be resized
SUPPORTED_VIDEO_TYPES = ['.mp4', '.avi', '.ogv', '.webm']

def resize_file(video_name: str, width: int, height: int, maintain_aspect_ratio: bool=True) -> None:
  """
  Resizes the specified video file.
  """
  video = mp.VideoFileClip(video_name)

  video_name, video_ext = os.path.splitext(video_name)
  video_resized = None

  if maintain_aspect_ratio:
    video_resized = video.resize(height=height)
  else:
    video_resized = video.resize(width=width, height=height)
  
  video_resized.write_videofile('{0}_resized{1}'.format(video_name, video_ext))

  print('Successfully resized 1 video.')

def resize_directory(path: str, width: int, height: int, maintain_aspect_ratio: bool=True) -> None:
  """
  Resizes all video files in the given directory.
  """
  resized = 0

  for f in os.listdir(path):
    f = os.path.join(path, f)
    file_name, file_ext = os.path.splitext(f)

    if os.path.isfile(f) and file_ext.lower() in SUPPORTED_VIDEO_TYPES:
      video = mp.VideoFileClip(f)
      video_resized = video.resize(height=height) if maintain_aspect_ratio else video.resize(width=width, height=height)
      video_resized.write_videofile('{0}_resized{1}'.format(file_name, file_ext))

      resized += 1
  print('Successfully resized {0} videos.'.format(resized))

if __name__ == '__main__':
  # Get video name or directory
  video_name = input('Please specify the video or directory to resize: ')

  # Maintaining aspect ratio?
  mari = input('Would you like to maintain aspect ratio?\nEnter YES/Y/NO/N: ').upper()
  maintain_aspect_ratio = None

  width = None

  # If we're maintaining aspect ratio, we'll use the height to calculate it.
  # Otherwise, get both the width and the height and scale the video to those values.
  if mari == 'YES' or mari == 'Y':
    maintain_aspect_ratio = True
  elif mari == 'NO' or mari == 'N':
    maintain_aspect_ratio = False
    width = input('Enter width or leave blank to use default of {0}: '.format(DEFAULT_WIDTH))
    width = DEFAULT_WIDTH if not width else int(width)
  else:
    print('Unrecognized input. Terminating program.')
    exit()
  height = input('Enter height or leave blank to use default of {0}: '.format(DEFAULT_HEIGHT))
  height = DEFAULT_HEIGHT if not height else int(height)

  # Handle video
  if os.path.isfile(video_name):
    resize_file(video_name, width, height, maintain_aspect_ratio)

  # Handle directory
  elif os.path.isdir(video_name):
    resize_directory(video_name, width, height, maintain_aspect_ratio)
  
  