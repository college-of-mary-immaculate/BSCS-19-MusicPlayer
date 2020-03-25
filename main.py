import tkinter as tk
from tkinter import filedialog
from tkinter import *
from pydub import AudioSegment
import random
import eyed3
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc

root = tk.Tk()
root.title("Music Player ♫")
root.geometry('506x470')
root.config(bg = 'gray30')
root.resizable(False,False)

class Player(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.Exit)
        self.m = 0
        self.s = -1
        self.ind = None
        self.pausePlayIcon = '▶'
        self.timeSeconds = None
        self.duration = None
        self.countSeconds = 0
        self.nextIfDoneHandle = None
        self.direction = "Down"

        self.bgFrame = Frame(self.master, bg = 'gray20', height = 351, width = 85)
        self.bgFrame.place(x= 0, y = 10)

        self.seperatorLabel = Label(self.bgFrame, text = ". .", font = ("calibri",45), bg = 'gray20', fg = 'ghostwhite')
        self.seperatorLabel.place(x= 17, y = 120)

        self.minuteLabel = Label(self.bgFrame, text = "0\n0", font = ("calibri",45), bg = 'gray20', fg = 'ghostwhite')
        self.minuteLabel.place(x= 25, y = 3)

        self.secondsLabel = Label(self.bgFrame, text = "0\n0", font = ("calibri",45), bg = 'gray20', fg = 'ghostwhite')
        self.secondsLabel.place(x= 25, y = 193)

        self.musicListFrame = Frame(self.master, height = 374, width = 420, borderwidth = 0, bg = 'gray20')
        self.musicListFrame.place(x = 94, y = 0)

        self.directoryFrame = Frame(self.musicListFrame, height = 30, width = 405, bg = 'gray45', borderwidth = 0)
        self.directoryFrame.place(x = 10, y = 10)

        self.folderButton = Button(self.directoryFrame, text = '🗀', font = ('impact', 20), fg = 'white', bg = 'gray45',
                            activeforeground = 'cyan', activebackground = 'gray45', borderwidth = 0,command = self.askdirctry)
        self.folderButton.place(x = 1, y = -17)

        self.directoryLabel = Label(self.directoryFrame, text = '← Choose a folder to look for .mp3 and .wav files.',font =('calibri',8), fg = 'white', bg = 'gray45')
        self.directoryLabel.place(x = 40, y = 6)

        self.listboxFrame = Frame(self.musicListFrame, borderwidth = 0, height = 500, width = 360, bg = 'gray')
        self.listboxFrame.place(x= 10, y = 40)

        self.scrollbar = Scrollbar(self.listboxFrame, orient = VERTICAL,bg = 'gray5')
        self.scrollbar.pack(side = 'right', fill = 'y')

        self.musicListBox = Listbox(self.listboxFrame,fg = 'white',bg = 'gray15', font = ('calibri',10),highlightthickness = 0,
                            selectbackground = 'cyan4', height = 20,width = 55,bd = 0,yscrollcommand = self.scrollbar.set)
        self.musicListBox.pack()

        self.scrollbar.config(command = self.musicListBox.yview)

        self.noMusicLabel = Label(self.musicListFrame, text = 'Please choose a folder first!', font =('calibri',12), fg = 'white', bg = 'gray15')
        self.noMusicLabel.place(x = 108, y = 190)

        self.playFrame = Frame(self.master, height = 62, width = 508, bg = 'gray45',borderwidth = 0)
        self.playFrame.place(x = 0, y = 372)
        
        self.progressFrame = Frame(self.playFrame, borderwidth = 0, height = 27, width = 505,bg = 'gray45' )
        self.progressFrame.place(x = 0, y = 0)
        
        self.totalTime = Label(self.progressFrame, text = 'Length: 00:00', fg = 'white',bg = 'gray45', font =('calibri',8))
        self.totalTime.place(x=429,y=3)
        
        self.barLine = Frame(self.progressFrame,borderwidth = 0, height = 3, width = 328, bg = 'gray55')
        self.barLine.place(x = 90, y = 11)

        self.songPlayingFrame = Frame(self.playFrame, borderwidth = 0, height = 42, width = 508,bg = 'gray45' )
        self.songPlayingFrame.place(x = 0, y = 20)
        
        self.artist = Label(self.songPlayingFrame, text = 'Artist', font = ('calibri',10,), fg = 'white', bg = 'gray45')
        self.artist.place(x = 97, y = 18)
        
        self.songName = Label(self.songPlayingFrame, text = 'Song Name or File Name', font = ('calibri',12,'bold'), fg = 'white', bg = 'gray45')
        self.songName.place(x = 97, y = -3)

        self.musicControlsFrame = Frame(self.master, height = 28, width = 508, bg = 'gray15')
        self.musicControlsFrame.place(x = 0, y = 438)

        #optional barLines in musicControlsFrame
        #self.barLine0 = Frame(self.musicControlsFrame,borderwidth = 0, height = 2, width = 150, bg = 'gray25')
        #self.barLine0.place(x = 90, y = 13)

        #self.barLine1 = Frame(self.musicControlsFrame,borderwidth = 0, height = 2, width = 170, bg = 'gray25')
        #self.barLine1.place(x = 345, y = 13)

        self.pauseAndPlayButton = Button(self.musicControlsFrame, text = self.pausePlayIcon, font = ('impact',18),fg = 'white', bg = 'gray15',state = DISABLED,
                        activeforeground = 'cyan4',activebackground = 'gray15',borderwidth = 0, command = self.pseply)
        self.pauseAndPlayButton.place(x = 278, y = -12)

        self.prevButton= Button(self.musicControlsFrame, text = '<', font = ('impact',17),fg = 'white', bg = 'gray15',state = DISABLED,
                        activeforeground = 'cyan4',activebackground = 'gray15',borderwidth = 0, command = self.Prevbtn)
        self.prevButton.place(x = 248, y = -8)

        self.nextButton= Button(self.musicControlsFrame, text = '>', font = ('impact',17),fg = 'white', bg = 'gray15',state = DISABLED,
                        activeforeground = 'cyan4',activebackground = 'gray15',borderwidth = 0, command = self.Nextbtn)
        self.nextButton.place(x = 314, y = -8)

        self.musicNoteFrame = Frame(self.master, height = 94, width = 94,borderwidth = 0)
        self.musicNoteFrame.place(x = 0, y = 372)

        self.noteIconLabel = Label(self.musicNoteFrame, text = '♫',fg = 'gray20', font = ('impact',40))
        self.noteIconLabel.place(x = 22, y = 8)

        self.noteDirIconLabel = Label(self.directoryFrame, text = "♫:", font = ('calibri',10), bg = 'gray45')
        self.noteDirIconLabel.place(x = 350, y = 4)

        self.musicCount = Label(self.directoryFrame, text = '0', font = ('calibri', 8), bg = 'gray45', fg = 'white')
        self.musicCount.place(x = 365, y = 6)

        self.tobeEnabledDisabled = [self.pauseAndPlayButton,self.prevButton,self.nextButton]

    def askdirctry(self):
        self.MUSICLIST = list()
        self.noteIconLabel.config(fg = 'gray20')
        self.folderButton.config(command = self.stopPlay)
        self.musicListBox.delete(0,tk.END)
        self.noMusicLabel.place(x = 108, y = 190)
        self.folderop = filedialog.askdirectory()

        if not self.folderop:
            self.musicListBox.unbind('<Double-Button-1>')
            self.folderButton.config(fg = 'white')
            self.directoryLabel.config(text = '← Choose a folder to look for .mp3 and .wav files.')
            self.noMusicLabel.config(text = 'Please choose a folder first!')
            self.musicCount.config(text = '0', fg = 'white')
            for y in self.tobeEnabledDisabled:
                y.config(state = DISABLED)
        else:
            if len(self.folderop) > 55:
                self.directoryLabel.config(text = '← ' + self.folderop[0:55]+'...')
            else:
                self.directoryLabel.config(text = '← ' + self.folderop)

            for x in os.listdir(self.folderop):
                if x.endswith('.mp3') or x.endswith('.wav'):
                    self.musicListBox.bind('<Double-Button-1>', self.Playm)
                    self.MUSICLIST.append(x)
                    self.folderButton.config(command = self.stopPlay)
                    self.folderButton.config(fg ='cyan')
                    self.noMusicLabel.place_forget()
                    self.musicListBox.insert(END, "   ♪  {0}".format(x))
                    self.musicListBox.config()
                else:
                    self.musicListBox.unbind('<Double-Button-1>')
                    self.folderButton.config(fg = 'white')
                    self.noMusicLabel.config(text = 'No songs found in this folder')
                    for y in self.tobeEnabledDisabled:
                        y.config(state = DISABLED)
            self.countsm = len(self.MUSICLIST)
            if self.countsm > 999:
                self.countsm = ('{0}+'.format(len(self.MUSICLIST)))
                self.musicCount.config(text = self.countsm, fg = 'cyan')
            elif self.countsm == 0:
                self.musicCount.config(text = self.countsm, fg = 'white')
            else:
                self.musicCount.config(text = self.countsm, fg = 'cyan')

    def proceedPlay(self):
        self.secondsLabel.config(text = "0\n0")
        self.minuteLabel.config(text = "0\n0")
        self.musicListBox.bind('<Double-Button-1>', self.Stopm)
        for x in self.tobeEnabledDisabled:
            x.config(state = NORMAL)

        self.musicListBox.selection_clear(0, END)
        self.musicListBox.selection_set(self.ind)
        self.musicListBox.activate(self.ind)
        
        self.fileChoice = self.MUSICLIST[self.ind]
        self.pathChoice = ("{0}\{1}".format(self.folderop,self.fileChoice))

        try:
            if self.fileChoice.endswith(".mp3"):
                self.MUSIC = eyed3.load(self.pathChoice)
                try:
                    self.songTitle = self.MUSIC.tag.title
                except:
                    self.songTitle = None
                
                if self.songTitle is None:
                    if len(self.fileChoice) > 50:
                        self.songTitle = ("{0}...".format(self.fileChoice[:50]))
                    else:
                        self.songTitle = self.fileChoice
                else:
                    if len(self.songTitle) > 50:
                        self.songTitle = ("{0}...".format(self.songTitle[:50]))
                self.songName.config(text = self.songTitle)

                try:
                    self.songArtist = self.MUSIC.tag.artist
                except:
                    self.songArtist = None
                    
                if self.songArtist is None:
                        self.songArtist = 'No artist'
                self.artist.config(text = self.songArtist)
                self.duration = self.MUSIC.info.time_secs

            elif self.fileChoice.endswith(".wav"):
                self.songTitle = self.fileChoice
                
                if len(self.songTitle) > 50:
                    self.songTitle = ("{0}...".format(self.songTitle[:50]))
                self.songName.config(text = self.songTitle)

                self.artist.config(text = "Wav file")

                wavFile = AudioSegment.from_file(self.pathChoice)
                self.duration = wavFile.duration_seconds
            
            
            self.timeSeconds = int(self.duration)
            self.mins, self.secs = divmod(self.duration,60)
            self.mins = round(self.mins)
            self.secs = round(self.secs)
            self.minuteSecond = ("Length: {:02d}:{:02d}".format(self.mins,self.secs))
            self.totalTime.config(text = self.minuteSecond)

            self.playMusic = vlc.MediaPlayer(self.pathChoice)
            self.pausePlayIcon = 'I I'
            self.noteIconLabel.config(fg ='cyan4')
            self.pauseAndPlayButton.config(text = self.pausePlayIcon, font = ('impact',13))
            self.pauseAndPlayButton.place(x = 282, y = -3)
            self.nextIfDone()
            self.playMusic.play()
            
        except:
            for y in self.tobeEnabledDisabled:
                y.config(state = DISABLED)
            self.noteIconLabel.config(fg = 'gray20')
            self.songName.config(text = "Error while trying to play the file!")
            self.artist.config(text = "Proceeding to the next song...")
            if self.direction == "Down":
                self.ind += 1
                if self.ind == len(self.MUSICLIST):
                    self.ind = 0
                    self.musicListBox.selection_set(0)
                    self.musicListBox.selection_set(0)
                    self.musicListBox.activate(0)
            elif self.direction == "Up":
                self.ind -= 1
                if self.ind == -1:
                    self.ind += len(self.MUSICLIST)
                    self.musicListBox.selection_clear(0, END)
                    self.musicListBox.selection_set(self.ind)
                    self.musicListBox.activate(self.ind)
            self.direction = "Down"
            self.master.after(3000,self.proceedPlay)

    def Playm(self, event):
        self.ind = self.musicListBox.index(ACTIVE)
        self.musicListBox.bind('<Double-Button-1>',self.Stopm)
        if self.nextIfDoneHandle:
            self.countSeconds = 0
            self.m = 0
            self.s = -1
            self.master.after_cancel(self.nextIfDoneHandle)
            self.nextIfDoneHandle = None
        self.proceedPlay()

    def Stopm(self,event):
        self.ind = self.musicListBox.index(ACTIVE)
        self.musicListBox.bind('<Double-Button-1>',self.Playm)
        if self.nextIfDoneHandle:
            self.m = 0
            self.s = -1
            self.countSeconds = 0
            self.master.after_cancel(self.nextIfDoneHandle)
            self.nextIfDoneHandle = None
        self.playMusic.stop()
        self.proceedPlay()

    def Nextbtn(self):
        self.direction = "Down"
        self.ind += 1
        self.playMusic.stop()
        if self.ind == len(self.MUSICLIST):
            self.ind = 0
        self.countSeconds = 0
        self.m = 0
        self.s = -1
        self.master.after_cancel(self.nextIfDoneHandle)
        self.proceedPlay()

    def Prevbtn(self):
        self.direction = "Up"
        self.ind -= 1
        self.playMusic.stop()
        if self.ind == -1:
            self.ind += len(self.MUSICLIST)
        self.countSeconds = 0
        self.m = 0
        self.s = -1
        self.master.after_cancel(self.nextIfDoneHandle)
        self.proceedPlay()
        
    def pseply(self):
        if self.pausePlayIcon == '▶':
            self.pausePlayIcon = 'I I'
            self.pauseAndPlayButton.config(text = self.pausePlayIcon, font = ('impact',13))
            self.pauseAndPlayButton.place(x = 282, y = -3)
            self.noteIconLabel.config(fg ='cyan4')
            self.nextIfDone()
            self.playMusic.play()
        elif self.pausePlayIcon == 'I I':
            self.pausePlayIcon = '▶'
            self.pauseAndPlayButton.config(text = self.pausePlayIcon, font = ('impact',18))
            self.pauseAndPlayButton.place(x = 278, y = -12)
            self.noteIconLabel.config(fg = 'gray20')
            self.master.after_cancel(self.nextIfDoneHandle)
            self.playMusic.pause()

    def stopPlay(self):
        for y in self.tobeEnabledDisabled:
            y.config(state = DISABLED)
        try:
            self.countSeconds = 0
            self.master.after_cancel(self.nextIfDoneHandle)
            self.playMusic.stop()
        except:
            pass
        self.askdirctry()

    def onShuffle(self):
        pass
    
    def nextIfDone(self):
        if self.countSeconds < self.timeSeconds:
            self.countSeconds += 1
            if self.s == 59:
                self.s = -1
                self.m += 1
            self.s += 1
            if len(str(self.s)) == 2:
                self.secondsLabel.config(text = "{0}\n{1}".format(str(self.s)[0], str(self.s)[1]))
            else:
                self.secondsLabel.config(text = "0\n{0}".format(self.s))
            if self.m > 0:
                if len(str(self.m)) == 2:
                    self.minuteLabel.config(text = "{0}\n{1}".format(str(self.m)[0], str(self.m)[1]))
                else:
                    self.minuteLabel.config(text = "0\n{0}".format(self.m))
            self.nextIfDoneHandle = self.master.after(1000, self.nextIfDone)
        elif self.countSeconds == self.timeSeconds:
            self.ind += 1
            self.m = 0
            self.s = -1
            self.countSeconds = 0
            self.musicListBox.selection_clear(0, END)
            self.musicListBox.selection_set(self.ind)
            self.musicListBox.activate(self.ind)
            if self.ind == len(self.MUSICLIST):
                self.ind = 0
                self.musicListBox.selection_set(0)
                self.musicListBox.selection_set(0)
                self.musicListBox.activate(0)
            self.nextIfDoneHandle = None
            self.proceedPlay()

    def Exit(self):
        try:
            self.master.after_cancel(self.nextIfDoneHandle)
            self.playMusic.stop()
        except:
            pass
        self.master.destroy()

Player(root).place()

root.mainloop()
