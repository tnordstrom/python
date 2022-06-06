# Tony Nordstrom
# May 28 2020 - June 8 2020
# Speed Typing Test
# From https://www.upgrad.com/blog/python-projects-ideas-topics-beginners/

# Progress report: May 28 2020
# Jotted down some implementation ideas
# Installed tkinter
# Created a basic application with all the required widgets
# Ran into problems creating the About box message widget
# This file is 103 lines long right now

# Progress report: May 29 2020
# Worked on the "About" box some more, it appears just once but won't disappear yet
# Attached event on keyrelease to call new function retrieve_input
# Imported time and difflib
# Started timing the duration of typing
# Started analysis of text differences using SequenceMatcher object in difflib

# Progress report: June 1 2020
# Added calculations for error count, word count, words per minute (raw and corrected)
# First attempt at detecting end of test, has some limitations (must have entered same # of characters as the reference doc)
# Getting the results update on the GUI during, and at the end of the test
# Testing and discovering the capabilities of the difflib SequenceMatcher tool
# - It looks like it can "forget" about errors as things progress
# - It is beyond the scope of this project to "fix" this tool, or write a replacement tool, so we're going to have to live with it.
# - autojunk=False option when creating the SequenceMatcher instance seems to help suppress this behaviour
# Now Start button clears the entered text, for support of subsequent test runs
# The file is 203 lines long right now

# Progress report: June 2 2020
# Testing, making small improvements
# Fixed the removal of the About box
# I'm finding I'm running out of things to do - maybe it is time for a new project?
# It would be nice to have a better way of detecting end-of-test, but what? I can't think of a better way. Exactly matching the end of text - what if there's errors?
# The file is 228 lines long right now

"""
Python Project Ideas: Advanced Level
31. Speed Typing Test
Let’s start advanced python project ideas for beginners.
Do you remember the old typing test game which was used in Windows XP and before?
You can create a similar program that tests your typing speed.
First, you need to create a UI using a library like Tkinter.
Then create a fun typing test that displays the user speed, accuracy and words per minute in the end.
You can also find source code for the program online.
"""

"""
Implementation Thoughts:
Display a couple of paragraphs of plain text. Display a timer, error counter, correct keystroke counter, raw speed, accuracy, words per minute
Controls: Begin test, Stop test, Reset results? Quit Program, About, Set Difficulty (set difficulty - offer more text examples - I will leave that as a future expansion)
Hit Begin test, timing won't start until the first key is pressed
Words per minute is the standard https://en.wikipedia.org/wiki/Words_per_minute 5 keystrokes, including spaces and punctuation
https://en.wikipedia.org/wiki/Speed_typing_contest for some interesting points, and an example typing sample
https://thepracticetest.com/typing/tests/practice-paragraphs/ has some good paragraphs
User speed is the raw words per minute, not considering accuracy
Accuracy is number of correct keys - number of mistakes / number of correct keys. This might be tricky to track properly.
For example, if the typist skips a letter, this should only count as one mistake, and the algorithm should be able to resynchronize to the following letter
Another example, if the typist adds a letter, this should also only count as one mistake
So maybe there should be a concept of "next target letter" X and "subsequent target letter" Y
If the typists entry matches Y before X, this is a likely skipped letter situation and X will be updated to the letter after Y.
For simplicity of algorithm, maybe I should limit skip detection to one deep.
Consider highlighting the paragraph as it is being typed, as feedback on the typist's progress
- That's too complex, and how to display errors? Have a seperate window, one for the paragraph, the other for the typing.
sudo apt install python3-tk to install tkinker. But I can't import Tkinter into my module. What's going on here? Oh it was capitalized in the example. WhoopS!
python -m tkinter to test that it works
https://docs.python.org/3/library/tkinter.html
https://web.archive.org/web/20190515141525/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/minimal-app.html
Question: is it legal to allow backspace, i.e. for the typist to correct their own mistakes on the fly? Or should backspace be disabled for this test?
For the purposes of this program, backspace (and delete) will be fully allowed, for simplicity. This also means the error rate will have to be recalculated as mistakes are corrected.
I seem to recall, in my high school typing class, that it was 5 words per mistake, and an incomplete word at the end of the test didn't count (either as a word or a mistake).
When does the test end? After a fixed time, or once all the text has been typed?
Thanks Stack Overflow for the hint about KeyRelease https://stackoverflow.com/questions/37097349/get-method-of-tkinter-text-widget-doesnt-return-the-last-character
https://docs.python.org/3/library/difflib.html for some differencing tools
word_count = len(text_input)/5
Corrected word count =- number of errors * 5?
https://stackoverflow.com/questions/50192923/strange-behaviour-of-python-difflib-library-for-sequence-matcher
Thanks Stack Overflow for the hint about turning junk behaviour off, getting more reliable error detection performance
https://stackoverflow.com/questions/23189610/remove-widgets-from-grid-in-tkinter
Thanks Stack Overflow for the hint about removing widgets from the grid - how to get grid_forget to actually work
"""

# Difficulty Level: 1.6 - 90 words
# From https://thepracticetest.com/typing/tests/practice-paragraphs/
practice_text = "Proofreader applicants are tested primarily on their spelling, speed, and skill in finding errors in the sample text. Toward that end, they may be given a list of ten or twenty classically difficult words and a proofreading test, both tightly timed. The proofreading test will often have a maximum number of errors per quantity of text and a minimum amount of time to find them. The goal of this approach is to identify those with the best skill set."


import tkinter as tk
import time
import difflib

about_text_displayed = False
time_started_typing = 0.0
time_stopped_typing = 0.0
word_count = 0
number_of_errors = 0
raw_words_per_minute = 0
corrected_words_per_minute = 0


class Application(tk.Frame):

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()
		self.matcher = difflib.SequenceMatcher(None, '', '', autojunk=False)
		self.matcher.set_seq1(practice_text)
		
	def display_about(self):
		global about_text_displayed
		about_text = "Speed Typing Test - By Tony Nordstrom"
		print(about_text)
		self.aboutDialog = tk.Message(self, text = about_text)
		self.aboutDialog.config(bg='lightgreen', font=('times', 24, 'italic'))
		if (about_text_displayed == False):
			self.aboutDialog.grid(row=9)
			about_text_displayed = True
		else:
			for x in self.grid_slaves():
				if int(x.grid_info()["row"]) > 8:
					x.grid_forget()
			about_text_displayed = False
		
	def start_test(self):
		global word_count
		global time_stopped_typing
		print("Start the test! Timing starts when you begin typing")
		# Focus should automatically be placed on the textEntry box
		self.textEntry.focus_set()
		self.textEntry.delete("1.0", tk.END)
		word_count = 0
		time_stopped_typing = 0.0
		
	def retrieve_input(self, event):
		global time_started_typing
		global word_count
		global number_of_errors
		global raw_words_per_minute
		global corrected_words_per_minute
		text_input = self.textEntry.get("1.0", tk.END)
		if(len(text_input) == 2):
			print("Just started")
			time_started_typing = time.time()
		else:
			print("Typing for ", time.time() - time_started_typing)
		word_count = len(text_input) // 5
		self.matcher.set_seq2(text_input)
		blocklist = self.matcher.get_matching_blocks()
		
		# Need to analyze the blocklist looking for mistake count
		# Is it a simple matter of counting the number of elements in the blocklist?
		# Even when I typed it perfectly, the list was of length two.
		number_of_errors = len(blocklist) - 2 # - 2 for First and Last Match	
		
		raw_words_per_minute = word_count / ((time.time() - time_started_typing) / 60)
		corrected_words_per_minute = (word_count - number_of_errors) / ((time.time() - time_started_typing) / 60)
		print(text_input)
		print(blocklist)
		print('word count', word_count)
		print('error count', number_of_errors)
		print('rWPM', raw_words_per_minute)
		print('cWPM', corrected_words_per_minute)
		
		# Update the gui while the test is in progress
		self.wordsPerMinute.configure(text=('Corrected WPM=%.2f' % corrected_words_per_minute))
		self.accuracy.configure(text=('Error Count=%d' % number_of_errors))
		self.rawSpeed.configure(text=('Raw WPM=%.2f' % raw_words_per_minute))
						
		# How to determine when the typing test is over?
		# If the number of characters in the reference string is equal to or less than the number of entered characters, end the test
		# Problem: What happens if errors have changed the length of the entered character so it is different than the reference string?
		# If the entered string is longer than the reference test, the test will be stopped "prematurely"
		# If the entered string is shorter than the reference test, the user will have to keep typing "garbage" to get to the end of test, or they could hit the stop button
		if(blocklist[-1].a <= blocklist[-1].b):
			print('Test complete')
			time_stopped_typing = time.time()
			self.stop_test()

	def stop_test(self):
		global time_started_typing
		global time_stopped_typing
		global word_count
		global number_of_errors
		global raw_words_per_minute
		global corrected_words_per_minute
		print("Stop the test!")
		if (time_stopped_typing == 0.0):
			time_stopped_typing = time.time()
		self.stopButton.focus_set()
		
		# Calculate final stats based on stop time
		raw_words_per_minute = word_count / ((time_stopped_typing - time_started_typing) / 60)
		corrected_words_per_minute = (word_count - number_of_errors) / ((time_stopped_typing - time_started_typing) / 60)

		# Update GUI with final numbers
		self.wordsPerMinute.configure(text=('Corrected WPM=%.2f' % corrected_words_per_minute))
		self.accuracy.configure(text=('Error Count=%d' % number_of_errors))
		self.rawSpeed.configure(text=('Raw WPM=%.2f' % raw_words_per_minute))
		
						
	def createWidgets(self):
		self.quitButton = tk.Button(self, text='Quit', command=self.quit)
		self.quitButton.grid()
		self.aboutButton = tk.Button(self, text='About', command=self.display_about)
		self.aboutButton.grid()
		self.startButton = tk.Button(self, text='Start', command=self.start_test)
		self.startButton.grid()
		self.stopButton = tk.Button(self, text='Stop', command=self.stop_test)
		self.stopButton.grid()
		self.practiceText = tk.Text(self, height = 5, width = 100)
		self.practiceText.grid()
		self.practiceText.insert(tk.END, practice_text)
		self.textEntry = tk.Text(self, height = 5, width = 100)
		self.textEntry.grid()
		self.textEntry.bind('<KeyRelease>', self.retrieve_input)
		self.wordsPerMinute = tk.Label(self, text='Corrected WPM=')
		self.wordsPerMinute.grid()
		self.accuracy = tk.Label(self, text="Error Count=")
		self.accuracy.grid()
		self.rawSpeed = tk.Label(self, text="Raw WPM=")
		self.rawSpeed.grid()
				
app = Application()
app.master.title('Speed Typing Test')
app.master.minsize(1000, 400)
app.mainloop()
