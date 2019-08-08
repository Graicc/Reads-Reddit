# Reads Reddit
A program to completely automate a YouTube channel.

## Setup

### Requirements

**Python Libraries:**
* [praw](https://praw.readthedocs.io/en/latest/)
* [gTTS](https://pypi.org/project/gTTS/)
* [mutagen.mp3](https://mutagen.readthedocs.io/en/latest/index.html)
* [PIL](https://pillow.readthedocs.io/en/stable/)

**Command Line Utilities:**
* [FFmpeg](https://ffmpeg.org/)
* [youtube-upload](https://github.com/tokland/youtube-upload)

Linux (for executing command line code. You might be able to get it working with windows)

### Installation

Make sure that you have all of the necessary requirements for each program before continuing (i.e. youtube-upload files).

After setting up a Reddit application [here](https://www.reddit.com/prefs/apps/), you must enter the data into a file titled `secrets.txt` as follows:

```
client_id
client_secret
user_agent
```

Additionally, you should create a `data.txt` file for the description, with the following information:

```
playlist_link (https://www.youtube.com/playlist?list=INSERT)
channel_sub_link (https://www.youtube.com/channel/INSERT?sub_confirmation=1)
```

After that it should be ready to run, by executing `video.py`.