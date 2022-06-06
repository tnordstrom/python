# Music Player

# June 4 2020 - June 8 2020
# https://www.upgrad.com/blog/python-projects-ideas-topics-beginners/#37_Music_Player
# http://effbot.org/tkinterbook/scale.htm for information on the scale widget used here for volume control
# https://www.tutorialspoint.com/sqlite/sqlite_python.htm
# https://docs.python.org/2/library/sqlite3.html

# June 4 2020 Progress Report
# Created a mind map outlining the app components
# Created a basic GUI
# Prompt user for base music directory
# Scan directory recursively for (music) files
# Started on: Populate a SQLite database with the file names, ran into some problems
# You can use ":memory:" to open a database connection to a database that resides in RAM instead of on disk - try this tomorrow?

# June 5 2020 Progress Report
# Split database initialization stuff into its own button function
# Finished successfully populating a database, used RAM for a bit then went back to using a file
# Created list gui elements for Artist, Album, Track lists
# Fills in all the track info with the help of TinyTag
# Selection supported for Artist, Album, and Track lists
# Problem: how do you keep a list selection even when selecting new lists? I want to see what I selected persist when I select another list
# Problem: some albums are full of tracks with the same title AFX Analogue Bubblebath - Untitled, as an example.
# Problem: If you delete the database, I don't know if the app handles that gracefully. It should just allow the database to be recreated.
# What's next: now I have a selected file to play, the play/pause button should play it! I don't know what Python module I should use to play music files.
# This file is now 198 lines long

# June 8 2020 Progress Report
# Using vlc library to play the music files
# Added text boxes to display currently playing artist, album, and track
# Filled in skip forwards, skip backwards, random, repeat functions
# Improved Play/Pause button functionality
# Problem: I can start multiple tracks at once, just by selecting them with the list and toggling pause/play again. I seem to lose control over the first track.
# Problem: About box blasts list boxes, make About box go away and it takes list boxes with it. Fixed.
# This file is now 336 lines long

# June 9 2020 Progress Report
# Fixed problem where I can start multiple tracks at once
# Fixed problem if database file is missing, was crashing, now just prints message to console
# Tried to fix issues with volume control, without much luck. At start volume control is 0, even though actual audio is higher
# TODO: Add a timing track control, display the track duration and time through, allow for navigating within the track
# Problem: Random can't be the first thing you press, - Fixed
# This file is now 361 lines long

# June 11 2020 Progress Report
# This is the first day working with talk radio on headphones, and interruptions every 30 minutes.
# I find it quite distracting
# Added Track Progress Scale, and Track Time and total Time Entry widgets
# Trying to get Track Progress Scale used as a control to set track progress, having problems. App is hanging.
# Changed Random to be a mode, at the end of a Random song, another Random song is selected
# This file is now 418 lines long

# June 12 2020 Progress Report
# Fixed a problem where Albums with the same name need to be qualified with Artist
# Not sure how to fix a problem where one track has album Dark Side Of The Moon and other tracks has album Dark Side of the Moon.
# - How to make selections case-insensitive?
# Skip forward and backward moves the track selection on Track list widget
# Not sure how to select Artist, Album, and Track in list widgets when Random file is selected
# - The problem is that the listbox widget has no method to select based on Text, just index, and I don't know how to convert Text to index.
# - I'm working on it. see "Work in progress" below.
# Problem: Sometimes skip forward / backward button hangs app. Not sure why.
# This file is now 456 lines long

# June 15 2020 Progress Report
# Finished Listview updates for random track selection
# Investigating hang during skip forward / backward. It seems to be the call self.player.stop()
# https://github.com/devkanro/Meta.Vlc/issues/3
# Suggests that pausing first then waiting a bit before sleep will avoid the problem. A sleep of 0.1 sec didn't seem to make a difference. Next time: try other delay times?
# hasattr player
# is playing
# now paused
# calling stop
# This file is now 500 lines long

# June 16 2020 Progress Report
# Looking at hang during stop
# https://forum.videolan.org/viewtopic.php?f=32&t=82502&p=272906&hilit=reentrant#p272906
# Tried a 1.0s delay but no difference
# Trying other approaches, use release instead of stop
# Not making any progress. I propose stopping work on this project and start a new project tomorrow.
# This file is now 512 lines long

import sys
print(sys.version)
import tkinter as tk
from tkinter import filedialog as fd
from tinytag import TinyTag

import glob
import sqlite3
import vlc
import random
from os import path
import time

about_text_displayed = False
playOrPause = True
Repeat = False
Random = False

selectedArtist = ""
selectedAlbum = ""
selectedTrack = ""
selectedFile = ""

class Application(tk.Frame):
	
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def display_about(self):
		global about_text_displayed
		about_text = "Music Player - By Tony Nordstrom"
		print(about_text)
		self.aboutDialog = tk.Message(self, text = about_text)
		self.aboutDialog.config(bg='lightgreen', font=('times', 24, 'italic'))
		if (about_text_displayed == False):
			self.aboutDialog.grid(row=12)
			about_text_displayed = True
		else:
			for x in self.grid_slaves():
				if int(x.grid_info()["row"]) > 11:
					x.grid_forget()
			about_text_displayed = False
	
	def play(self, ForcePlay):
		global playOrPause
		if (ForcePlay == True):
			playOrPause = True
		if (playOrPause == True):
			print('Play')
			self.player.play()
			playOrPause = False
			self.playButton['text'] = "Pause"
			#volume = self.player.audio_get_volume()
			#print('Volume control set to', volume)
			#self.VolumeControl.set(volume)
		else:
			print('Pause')
			self.player.pause()
			playOrPause = True
			self.playButton['text'] = "Play"

	def skip_forwards(self):
		print('Skip forwards')
		global selectedAlbum
		global selectedTrack
		global selectedFile
		print('Selected track is ', selectedTrack, ' next track is')
		conn = sqlite3.connect('music.db')
		# Load the filename for that track from the database
		for row in conn.execute('SELECT * FROM MUSIC WHERE ALBUM=? AND NAME=?', (selectedAlbum,selectedTrack,)):
			track_number = row[5]
		for row in conn.execute('SELECT * FROM MUSIC WHERE ALBUM=? AND TRACK_NO=?', (selectedAlbum,track_number+1,)):
			print(row)
			print('after printing row')
			if (hasattr(self, 'player')):
				print('hasattr player')
				if (self.player.is_playing()):
					print('is playing')
					# https://github.com/devkanro/Meta.Vlc/issues/3 Suggests that pausing - delay - then stop is a good workaround
					#self.player.pause()
					#print('now paused')
					#time.sleep(1)
					print('calling stop')
					self.player.stop()
					self.player.release()
					print('stop seems to be the problem')
			selectedTrack = row[1]
			print('selectedTrack', row[1])
			selectedFile = row[2]
			print('selectedFile', row[2])
			current_index = self.TrackList.curselection()[0]
			print('current index', current_index)
			self.TrackList.selection_clear(current_index,None)
			self.TrackList.selection_set(current_index+1,None)
			self.TrackList.see(current_index+1)
			self.player = vlc.MediaPlayer(selectedFile)
			print('self.player created')
			em = self.player.event_manager()
			em.event_attach(vlc.EventType.MediaPlayerEndReached, self.endTrack)
			em.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.TrackProgressUpdate)
			print('event_attach complete')
			self.CurrentTrack.delete(0, tk.END)
			self.CurrentTrack.insert(0, selectedTrack)
			print('self.play(True)')
			self.play(True)
		conn.close()
		
	def skip_backwards(self):
		print('Skip backwards')
		global selectedAlbum
		global selectedTrack
		global selectedFile
		print('Selected track is ', selectedTrack, ' next track is')
		conn = sqlite3.connect('music.db')
		# Load the filename for that track from the database
		for row in conn.execute('SELECT * FROM MUSIC WHERE ALBUM=? AND NAME=?', (selectedAlbum,selectedTrack,)):
			track_number = row[5]
		for row in conn.execute('SELECT * FROM MUSIC WHERE ALBUM=? AND TRACK_NO=?', (selectedAlbum,track_number-1,)):
			print(row)
			if (self.player.is_playing()):
				self.player.stop()
			selectedTrack = row[1]
			selectedFile = row[2]
			current_index = self.TrackList.curselection()[0]
			self.TrackList.selection_clear(current_index,None)
			self.TrackList.selection_set(current_index-1,None)
			self.TrackList.see(current_index-1)
			self.player = vlc.MediaPlayer(selectedFile)
			em = self.player.event_manager()
			em.event_attach(vlc.EventType.MediaPlayerEndReached, self.endTrack)
			em.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.TrackProgressUpdate)
			self.CurrentTrack.delete(0, tk.END)
			self.CurrentTrack.insert(0, selectedTrack)
			self.play(True)
		conn.close()
				
	def random(self):
		global Random
		if (Random == False):
			print('Random')
			self.random_play()
			Random = True
			self.RandomButton['text'] = "No Random"
		else:
			print('No Random')
			Random = False
			self.RandomButton['text'] = "Random"
	
	def random_play(self):
		print('Random')
		global selectedArtist
		global selectedAlbum
		global selectedTrack
		global selectedFile
		random_id = random.randint(0, 5080) # What's the maximum ID in the database? I cheated and looked at the debug information
		conn = sqlite3.connect('music.db')
		for row in conn.execute('SELECT * FROM MUSIC WHERE ID=?', (random_id,)):
			print(row)
			if (hasattr(self, 'player')):
				if (self.player.is_playing()):
					self.player.stop()
			selectedTrack = row[1]
			selectedFile = row[2]
			selectedAlbum = row[3]
			selectedArtist = row[4]
			# Update Listbox objects with random selection: Artist List
			index = range(0, self.ArtistList.size())
			for n in index:
				if selectedArtist == self.ArtistList.get(n):
					self.ArtistList.selection_clear(0, tk.END)
					self.ArtistList.selection_set(n)
					self.ArtistList.see(n)
			# Update Album List object:
			# Clear Album List first
			self.AlbumList.delete(0, tk.END) # Get rid of old entries
			for x in conn.execute('SELECT * FROM MUSIC WHERE ARTIST=?', (selectedArtist,)):
				print(x)
				listexisting = self.AlbumList.get(0, tk.END)
				if x[3] not in listexisting:
					self.AlbumList.insert(tk.END, x[3])
			index = range(0, self.AlbumList.size())		
			for n in index:
				if selectedAlbum == self.AlbumList.get(n):
					self.AlbumList.selection_clear(0, tk.END)
					self.AlbumList.selection_set(n)
					self.AlbumList.see(n)
			# Next do the track list
			self.TrackList.delete(0, tk.END) # Get rid of old entries
			for y in conn.execute('SELECT * FROM MUSIC WHERE ARTIST=? AND ALBUM=?', (selectedArtist,selectedAlbum)):
				print(y)
				listexisting = self.TrackList.get(0, tk.END)
				if y[1] not in listexisting:
					self.TrackList.insert(tk.END, y[1])
			index = range(0, self.TrackList.size())		
			for n in index:
				if selectedTrack == self.TrackList.get(n):
					self.TrackList.selection_clear(0, tk.END)
					self.TrackList.selection_set(n)
					self.TrackList.see(n)
			# Create new MediaPlayer instance with random selected file
			self.player = vlc.MediaPlayer(selectedFile)
			em = self.player.event_manager()
			em.event_attach(vlc.EventType.MediaPlayerEndReached, self.endTrack)
			em.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.TrackProgressUpdate)
			self.CurrentArtist.delete(0, tk.END)
			self.CurrentArtist.insert(0, selectedArtist)
			self.CurrentAlbum.delete(0, tk.END)
			self.CurrentAlbum.insert(0, selectedAlbum)
			self.CurrentTrack.delete(0, tk.END)
			self.CurrentTrack.insert(0, selectedTrack)
			self.play(True)
		conn.close()

	def repeat(self):
		global Repeat
		if (Repeat == True):
			print('Repeat off')
			Repeat = False
			self.RepeatButton['text'] = "Repeat"
		else:
			print('Repeat on')
			Repeat = True
			self.RepeatButton['text'] = "No Repeat"
		
	@vlc.callbackmethod
	def endTrack(self, event):
		global Repeat
		global selectedFile
		print('Track has ended')
		# What to do next depends on repeat mode
		if (Repeat == True):
			self.player = vlc.MediaPlayer(selectedFile)
			em = self.player.event_manager()
			em.event_attach(vlc.EventType.MediaPlayerEndReached, self.endTrack)
			em.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.TrackProgressUpdate)
			self.player.play()
		elif (Random == True):
			self.random_play()
		else:
			self.skip_forwards()
		
	def UpdateVolume(self, event):
		volume = self.VolumeControl.get()
		if (hasattr(self, 'player')):
			print('Volume set to', volume)
			self.player.audio_set_volume(volume)

	def ArtistSelected(self, event):
		global selectedArtist
		selectedArtist = self.ArtistList.get(self.ArtistList.curselection())
		self.CurrentArtist.delete(0, tk.END)
		self.CurrentArtist.insert(0, selectedArtist)
		print('Selected artist is ', selectedArtist)
		# Fill in the album list now
		self.AlbumList.delete(0, tk.END) # Get rid of old entries
		conn = sqlite3.connect('music.db')
		#for row in conn.execute('SELECT * FROM MUSIC ORDER BY ALBUM WHERE ARTIST=?', (selectedArtist,)):
		for row in conn.execute('SELECT * FROM MUSIC WHERE ARTIST=?', (selectedArtist,)):
			print(row)
			listexisting = self.AlbumList.get(0, tk.END)
			if row[3] not in listexisting:
				self.AlbumList.insert(tk.END, row[3])
		conn.close()

	def AlbumSelected(self, event):
		global selectedAlbum
		global selectedArtist
		selectedAlbum = self.AlbumList.get(self.AlbumList.curselection())
		self.CurrentAlbum.delete(0, tk.END)
		self.CurrentAlbum.insert(0, selectedAlbum)
		print('Selected album is ', selectedAlbum)
		# Fill in the track list now
		self.TrackList.delete(0, tk.END) # Get rid of old entries
		conn = sqlite3.connect('music.db')
		for row in conn.execute('SELECT * FROM MUSIC WHERE ARTIST=? AND ALBUM=?', (selectedArtist,selectedAlbum)):
			print(row)
			listexisting = self.TrackList.get(0, tk.END)
			if row[1] not in listexisting:
				self.TrackList.insert(tk.END, row[1])
		conn.close()
		
	def TrackSelected(self, event):
		global selectedAlbum
		global selectedTrack
		global selectedFile
		global playOrPause
		selectedTrack = self.TrackList.get(self.TrackList.curselection())
		self.CurrentTrack.delete(0, tk.END)
		self.CurrentTrack.insert(0, selectedTrack)
		print('Selected track is ', selectedTrack)
		# Now we're ready to play music!
		conn = sqlite3.connect('music.db')
		# Load the filename for that track from the database
		for row in conn.execute('SELECT * FROM MUSIC WHERE ALBUM=? AND NAME=?', (selectedAlbum,selectedTrack,)):
			print(row[2])
			# What if there's more than one match at this point? Could happen that there are more than one track with the same name.
			selectedFile = row[2]
			if (hasattr(self, 'player')):
				if (self.player.is_playing()):
					self.player.stop() # Stop any existing playing file
			self.player = vlc.MediaPlayer(selectedFile)
			em = self.player.event_manager()
			em.event_attach(vlc.EventType.MediaPlayerEndReached, self.endTrack)
			em.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.TrackProgressUpdate)
			self.play(True)
		conn.close()
				
	def loadDatabase(self):
		# Specifying the root directory, scanning, and populating the database is something that should only need to be done once,
		# or on demand. Once it's set up, it should just be a matter of using the database
		self.RootDirectory = fd.askdirectory()
		print(self.RootDirectory)
		musicfiles = glob.glob(self.RootDirectory + "/**/*.mp3", recursive=True)
		musicfiles.extend(glob.glob(self.RootDirectory + "/**/*.m4a", recursive=True))
		for x in musicfiles:
			print(x)
		print(len(musicfiles))
		conn = sqlite3.connect('music.db') # Later use a file on disk to store the database: for now, just use RAM. Allows the table to be created each time the program is run.
		#conn = sqlite3.connect(':memory:')
		print("Opened database successfully")
		conn.execute('''CREATE TABLE MUSIC
					(ID INT PRIMARY KEY		NOT NULL,
					NAME		TEXT		,
					FILE		TEXT		NOT NULL,
					ALBUM		TEXT		,
					ARTIST		TEXT		,
					TRACK_NO	INT			,
					TOTAL_TR	INT 		);''')
		print("Table created successfully")
		id = 0
		for x in musicfiles:
			print('Inserting FILE ', x, ' ID ', id, ' into Database')
			tag = TinyTag.get(x)
			conn.execute("INSERT INTO MUSIC (FILE, ID, NAME, ALBUM, ARTIST, TRACK_NO, TOTAL_TR) VALUES (?,?,?,?,?,?,?)", (x, id, tag.title, tag.album, tag.artist, tag.track, tag.track_total));
			id = id+1
		conn.commit()
		print("Records created successfully")
		# Fill in the artist list before leaving
		for row in conn.execute('SELECT * FROM MUSIC ORDER BY ARTIST'):
			print(row)
			listexisting = self.ArtistList.get(0, tk.END)
			if row[4] not in listexisting:
				self.ArtistList.insert(tk.END, row[4])
		conn.close()
		
	def TrackScan(self, event):
		print('Track Scan')
		position = self.TrackProgress.get()
		if (hasattr(self, 'player')):
			#em = self.player.event_manager()
			#em.event_detach(vlc.EventType.MediaPlayerPositionChanged)
			print('Track position set to', position)
			#self.player.set_position(position) # What does this really do?
			#em.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.TrackProgressUpdate)
						
	@vlc.callbackmethod
	def TrackProgressUpdate(self, event):
		position = self.player.get_position()
		print('TrackProgressUpdate position', position)
		self.TrackProgress.set(position * 100)
		millisec = self.player.get_time()
		track_time = '%d:%02.3f' % ((millisec/1000)/60, (millisec/1000)%60)
		millisec = self.player.get_length()
		track_total = '%d:%02.3f' % ((millisec/1000)/60, (millisec/1000)%60)
		self.TrackTime.delete(0, tk.END)
		self.TrackTime.insert(0, track_time)
		self.TrackTotal.delete(0, tk.END)
		self.TrackTotal.insert(0, track_total)
		
	def createWidgets(self):
		self.quitButton = tk.Button(self, text='Quit', command=self.quit)
		self.quitButton.grid()
		self.aboutButton = tk.Button(self, text='About', command=self.display_about)
		self.aboutButton.grid()
		self.playButton = tk.Button(self, text='Play', command=lambda: self.play(False))
		self.playButton.grid()
		self.skipForwardsButton = tk.Button(self, text='Skip Forwards', command=self.skip_forwards)
		self.skipForwardsButton.grid()
		self.skipBackwardsButton = tk.Button(self, text='Skip Backwards', command=self.skip_backwards)
		self.skipBackwardsButton.grid()	
		self.RandomButton = tk.Button(self, text='Random', command=self.random)
		self.RandomButton.grid()				
		self.RepeatButton = tk.Button(self, text='Repeat', command=self.repeat)
		self.RepeatButton.grid()
		self.LoadDatabaseButton = tk.Button(self, text='Database', command=self.loadDatabase)
		self.LoadDatabaseButton.grid()
		self.VolumeControl = tk.Scale(self, from_=100, to_=0, command=self.UpdateVolume)
		self.VolumeControl.grid()
		self.ArtistList = tk.Listbox(self, exportselection=0, width=50)
		self.ArtistList.bind("<<ListboxSelect>>", self.ArtistSelected)
		self.ArtistList.grid()
		self.AlbumList = tk.Listbox(self, exportselection=0, width=50)
		self.AlbumList.bind("<<ListboxSelect>>", self.AlbumSelected)
		self.AlbumList.grid()
		self.TrackList = tk.Listbox(self, exportselection=0, width=50)
		self.TrackList.bind("<<ListboxSelect>>", self.TrackSelected)
		self.TrackList.grid()
		self.CurrentArtist = tk.Entry(self, width=50)
		self.CurrentArtist.grid(column=1, row=0)
		self.CurrentAlbum = tk.Entry(self, width=50)
		self.CurrentAlbum.grid(column=1, row=1)
		self.CurrentTrack = tk.Entry(self, width=50)
		self.CurrentTrack.grid(column=1, row=2)
		self.TrackProgress = tk.Scale(self, from_=0, to_=100, length=400, resolution=0.1, orient=tk.HORIZONTAL, command=self.TrackScan)
		self.TrackProgress.grid(column=1, row=3)
		self.TrackTime = tk.Entry(self, width=10)
		self.TrackTime.grid(column=1, row=4)
		self.TrackTotal = tk.Entry(self, width=10)
		self.TrackTotal.grid(column=1, row=5)
		
		# Open database if it exists, load the artist list
		if path.exists('music.db'):
			conn = sqlite3.connect('music.db')
			# Fill in the artist list
			for row in conn.execute('SELECT * FROM MUSIC ORDER BY ARTIST'):
				print(row)
				listexisting = self.ArtistList.get(0, tk.END)
				if row[4] not in listexisting:
					self.ArtistList.insert(tk.END, row[4])
			conn.close()
		else:
			print("Database file missing: Recreate database")
					
app = Application()
app.master.title('Music Player')
app.master.minsize(1000, 400)
app.mainloop()
