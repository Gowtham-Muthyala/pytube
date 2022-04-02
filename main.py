from pytube import YouTube, Playlist
import re
import sys

class bgcolors:
    OKGREEN = '\033[92m' #GREEN
    OKBLUE = '\033[94m' #BLUE
    OKCYAN = '\033[96m' #CYAN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    BOLD = '\033[1m' #BOLD
    UNDERLINE = '\033[4m' #UNDERLINE

# Capturing Input from USER (URL -> Single Video/Playlist)
url = input("Please Paste  your YouTube URL to download : ")

file_size = 0

# This Function is responsible to show the Download Progress of Video/s
# taken Reference from https://github.com/pytube/pytube/issues/749 and modified some points
def progress(stream, _chunk, bytes_remaining):
    global file_size
    current = ((stream.filesize - bytes_remaining)/stream.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    file_size = stream.filesize/1024000
    sys.stdout.write(' ↳ '+ bgcolors.OKGREEN +'|{bar}| {percent}% [{currentMB} MB / {file_size} MB]\r'.format(
        bar=status, percent=percent, currentMB=round(file_size-(bytes_remaining/1024000), 2), file_size=round(file_size, 2))+bgcolors.RESET)
    sys.stdout.flush()

def single_video_download(video):
  count = 1
  if aud_vid == "2":
    videos_format = yt.streams.filter(progressive=True)
    print(bgcolors.OKCYAN + "Available Formats : " + bgcolors.RESET)
    for i in videos_format:
      print(bgcolors.WARNING + f"{count}. {i.mime_type} -> {i.resolution} x {i.fps}fps" + bgcolors.RESET)
      count += 1
    res_aud_selected = input("Please select any one option from above for your download : ")
    filtering = videos_format[int(res_aud_selected)-1]
    resolution_fps = str(filtering.resolution) + " x " + str(filtering.fps) + "fps"
  elif aud_vid =="1":
    videos_format = yt.streams.filter(only_audio=True)
    print(bgcolors.OKCYAN + "Available Formats : " + bgcolors.RESET)
    for i in videos_format:
      print(bgcolors.WARNING + f"{count}. {i.mime_type} -> {i.abr}" + bgcolors.RESET)
      count += 1
    res_aud_selected = input("Please select any one option from above for your download : ")
    filtering = videos_format[int(res_aud_selected)-1]
    resolution_fps = str(filtering.abr)

  print(bgcolors.WARNING + 'downloading :' + bgcolors.RESET + ' {} with url : {}'.format(yt.title, yt.watch_url), end = " ")
  yt.register_on_progress_callback(progress)
  print(bgcolors.OKGREEN + "[{}]".format(resolution_fps) + bgcolors.RESET)
  filtering.download("Downloads")
  print(bgcolors.OKCYAN + 
      f"Download Completed Successfully - '{yt.title}' -> [{round(file_size,2)}MB]\t\t\t\t\t\t\t\t" + bgcolors.RESET)

# This Block is responsible to differentiate Playlist with Single Video
# If the provided URL is Playlist Then it will go through all the Videos in the list and download one by one and
# 			create a folder with Playlist name in youtube in download folder
# Else if it is an individual video then it will download automatically in the Downloads Folder in the same directory of the Code exists

if 'list' in url.lower():
  playlist = Playlist(url)
  print('Number of videos available in playlist: %s' % len(playlist.video_urls))
  aud_vid = input("You want to download the request in " + bgcolors.WARNING + "Audio(1) or Video(2) " + bgcolors.RESET + "-" + bgcolors.FAIL + " Enter [1/2] Only" + bgcolors.RESET + " : ")
  if "index=" in url.lower():
    index = int(re.findall(r'\d*$', url)[0]) - 1
    single_video_download(playlist.videos[index])
  else:
    for video in playlist.videos:
      lst_val = video
      if aud_vid == "2":
        print(bgcolors.WARNING + 'downloading :' + bgcolors.RESET + ' {} with url : {}'.format(
            lst_val.title, lst_val.watch_url), end = " ")
        lst_val.register_on_progress_callback(progress)
        filtering = lst_val.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        resolution_fps = str(filtering.resolution) + " x " + str(filtering.fps) + "fps"
        print(bgcolors.OKGREEN + "[{}]".format(resolution_fps) + bgcolors.RESET)
      elif aud_vid == "1":
        print(bgcolors.WARNING + 'downloading :' + bgcolors.RESET + ' {} with url : {}'.format(
            lst_val.title, lst_val.watch_url), end = " ")
        lst_val.register_on_progress_callback(progress)
        filtering = lst_val.streams.filter(only_audio=True).order_by('abr').desc().first()
        resolution_fps = "audio -- "+str(filtering.abr)
        print(bgcolors.OKGREEN + "[{}]".format(resolution_fps) + bgcolors.RESET)
      
      filtering.download(f"Downloads/{playlist.title}")
      print(bgcolors.OKCYAN +
          f"Downloaded successfully '{lst_val.title}' -> [{round(file_size,2)}MB]\t\t\t\t\t\t\n" + bgcolors.RESET)

else:
  yt = YouTube(url)
  aud_vid = input("You want to download the request in " + bgcolors.WARNING + "Audio(1) or Video(2) " + bgcolors.RESET + "-" + bgcolors.FAIL + " Enter [1/2] Only" + bgcolors.RESET + " : ")
  single_video_download(yt)