# Reddit parts
import time
from random import randrange
class Text:
	def __init__(self, post, title = False):
		if title:
			self.body = post.title
		else:
			self.body = post.body
		if not post.author:
			self.author = "[Deleted]"
		else:
			self.author = post.author.name
		self.uid = post.permalink

import praw
def GetReddit():
	print("Loggin in ...")
	f = open("secrets.txt", "r")
	r = praw.Reddit(client_id=f.readline().strip(), client_secret=f.readline().strip(), user_agent=f.readline().strip())
	f.close()
	print("Logged in\n")

	print("Getting thread ....")
	for i in r.subreddit('AskReddit').top('day'):
		post = i
		break
	print("Thread got\n")

	title = Text(post, True)
	print("Title: {}".format(title.body))

	post.comment_sort = 'best'
	comments = []
	for i in range(0,20):
		comments.append(Text(post.comments[i], False))
		print("comment {0}: u/{1.author} {2}".format(i, comments[-1], comments[-1].body[:50]))
	return title, comments

def GetText(toScrape):
	text = []
	for t in toScrape:
		text.append(t.body)
	return text

# Image parts
import textwrap
import copy
from PIL import Image, ImageDraw, ImageFont
tFont = ImageFont.truetype('Fonts/IBMPlexSans.ttf', size = 100)
bFont = ImageFont.truetype('Fonts/NotoSans.ttf', size = 50)
wFont = ImageFont.truetype('Fonts/Righteous.ttf', size = 12)

def DrawComment(comment, number, comments):
	print("Rendering img #{}".format(number))

	wrappedText = textwrap.wrap(comment.body, width = 70)
	if len(wrappedText) > 14:
		print("splitting comment")
		lastLine = wrappedText[13]
		splitPoint = comment.body.find(lastLine) + len(lastLine) + 1
		page1 = comment.body[0:splitPoint]
		page2 = comment.body[splitPoint:]
		wrappedText = textwrap.wrap(page1, width = 70)
		newComment = copy.deepcopy(comment)
		comment.body = page1
		newComment.body = page2
		comments.insert(number + 1, newComment)

	img = Image.new('RGB', (1920, 1080), color = "hsl({}, 100%, 90%)".format(randrange(0,360,36)))

	d = ImageDraw.Draw(img)
	d.text((20, 0), "u/{}".format(comment.author), fill = (0,0,0), font = tFont)
	
	offset = 130
	for line in wrappedText:
		d.text((20, offset), line, fill = (0,0,0), font = bFont)
		offset += bFont.getsize(line)[1]

	d.text((1835, 1060), "ReadsReddit", fill = (191, 191, 191), font = wFont)

	img.save("img/{0:03d}.png".format(number))

	return comments

# TTS parts
from gtts import gTTS
from mutagen.mp3 import MP3
def RenderAudio(text, number):
	print("Rendering audio #{}".format(number))
	gTTS(text, 'en').save("audio/{0:03d}.mp3".format(number))
	audio = MP3("audio/{0:03d}.mp3".format(number))
	
	return audio.info.length

# FFMPEG parts
def GenerateInput(lengths):
	print("Generating input config file\n")
	file = open("input.txt", "w")
	for i in lengths:
		file.write("file 'img/{0:03d}.png'\nduration {1}\n".format(lengths.index(i), i))
	file.write("file 'img/{0:03d}.png'".format(len(lengths) - 1))

def GenerateInputa(len):
	print("Generating audio input config file\n")
	file = open("inputa.txt", "w")
	for i in range(0, len):
		file.write("file 'audio/{0:03d}.mp3'\n".format(i))

import os
def Export(len, lengths):
	GenerateInput(lengths)
	GenerateInputa(len)
	os.system("ffmpeg -f concat -i input.txt -f concat -i inputa.txt -c:v libx264 -c:a aac -b:a 192k -shortest -vsync vfr -pix_fmt yuv420p output.mp4 -y")

# Youtube parts
def Upload(titleClass):
	tText = titleClass.body
	if len(tText) > 81:
		tText = tText[0:82] + "..."
	title = "{} - Reads Reddit".format(tText)
	print(title)

	f = open("data.txt", "r")
	desc = "r/AskReddit - {0.body} (https://www.reddit.com{0.uid}) \
		\n\nPlaylist: {1} \
		\nDon't forget so subscribe: {2}" \
		.format(titleClass, f.readline().strip(), f.readline().strip())
	
	f.close()
	print(desc)

	print('youtube-upload --title="{0}" \
--description="{1}" \
--category="Entertainment" \
--playlist="Reddit Read" \
--tags="reddit, reading, stories, sharing" \
--thumbnail="img/001.png" \
output.mp4'.format(title, desc))
	os.system('youtube-upload --title="{0}" \
		--description="{1}" \
		--category="Entertainment" \
		--playlist="Reddit Read" \
		--tags="reddit, reading, stories, sharing" \
		--thumbnail="img/001.png" \
		output.mp4'.format(title, desc))

import shutil
def CleanUp():
	print("Cleaning up")
	shutil.rmtree("audio")
	shutil.rmtree("img")
	os.remove("input.txt")
	os.remove("inputa.txt")
	os.remove("output.mp4")
	print("Cleaned up")

def main():
	title, comments = GetReddit() # Get data from Reddit
	comments.insert(0, title)

	if not os.path.exists("img"): # Create the image folder if it does not already exist
		os.makedirs("img")

	j = 0
	while j < len(comments): # Draw all of the comments, done safely becuase of multi-page comments
		i = comments[j]
		comments = DrawComment(i, j, comments)
		j += 1

	if not os.path.exists("audio"): # Create the audio folder if it does not already exist
		os.makedirs("audio")
	
	lengths = []
	for i, comment in enumerate(comments): # Render all of the audio
		length = RenderAudio(comment.body, i)
		lengths.append(length)

	Export(len(comments), lengths) # Render and upload the video
	Upload(title)
	
	CleanUp() # Basic cleanup, removes audio and image folders

if __name__== "__main__":
	main()
