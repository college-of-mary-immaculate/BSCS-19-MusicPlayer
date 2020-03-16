import tkinter as tk
from tkinter import filedialog
from tkinter import *
import eyed3
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc

root = tk.Tk()
root.title("Music Player ♫")
root.geometry('508x470')
root.config(bg = 'gray30')
root.resizable(False,False)

class Player(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master = master
        self.ind = None
        self.pausePlayIcon = '▶'

        self.temporaryBar1 = Frame(self.master, height = 350, width = 32, bg = 'gray20')
        self.temporaryBar1.place(x = 10, y = 0)

        self.barLine0 = Frame(self.master,borderwidth = 0, height = 100, width = 3, bg = 'gray45')
        self.barLine0.place(x = 15, y = 0)
        
        self.temporaryBar2 = Frame(self.master, height = 325, width = 32, bg = 'gray20')
        self.temporaryBar2.place(x = 53, y = 0)

        self.barLine1 = Frame(self.master,borderwidth = 0, height = 150, width = 3, bg = 'gray45')
        self.barLine1.place(x = 58, y = 250)

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

        self.musicListBox = Listbox(self.listboxFrame,fg = 'white',bg = 'gray15', font = ('calibri',10),highlightcolor  = 'gray15',
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
        self.totalTime.place(x=431,y=3)
        
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

    def askdirctry(self):
        self.MUSICLIST = list()
        self.noteIconLabel.config(fg = 'gray20')
        self.barLine0.config(bg = 'gray45')
        self.barLine1.config(bg = 'gray45')
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
            self.tobedisabled = [self.pauseAndPlayButton,self.prevButton,self.nextButton]
            for y in self.tobedisabled:
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
                    self.tobedisabled = [self.pauseAndPlayButton,self.prevButton,self.nextButton]
                    for y in self.tobedisabled:
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
        self.musicListBox.bind('<Double-Button-1>', self.Stopm)
        self.toBeEnabled = [self.pauseAndPlayButton, self.prevButton,self.nextButton]
        for x in self.toBeEnabled:
            x.config(state = NORMAL)
        
        self.fileChoice = self.MUSICLIST[self.ind]
        self.pathChoice = ("{0}\{1}".format(self.folderop,self.fileChoice))

        if self.fileChoice.endswith(".mp3"):
            self.MUSIC = eyed3.load(self.pathChoice)
            self.songTitle = self.MUSIC.tag.title
            
            if self.songTitle == None:
                if len(self.fileChoice) > 50:
                    self.songTitle = ("{0}...".format(self.fileChoice[:50]))
                else:
                    self.songTitle = self.fileChoice
            else:
                if len(self.songTitle) > 50:
                    self.songTitle = ("{0}...".format(self.songTitle[:50]))
            self.songName.config(text = self.songTitle)

            self.songArtist = self.MUSIC.tag.artist
            if self.songArtist == None:
                    self.songArtist = 'No artist'
            self.artist.config(text = self.songArtist)

        elif self.fileChoice.endswith(".wav"):
            self.songTitle = self.fileChoice
            
            if len(self.songTitle) > 50:
                self.songTitle = ("{0}...".format(self.songTitle[:50]))
            self.songName.config(text = songTitle)

            self.artist.config(text = "Wav file")

        self.duration = self.MUSIC.info.time_secs
        self.mins, self.secs = divmod(self.duration,60)
        self.mins = round(self.mins)
        self.secs = round(self.secs)
        self.minuteSecond = ("Length: {:02d}:{:02d}".format(self.mins,self.secs))
        self.totalTime.config(text = self.minuteSecond)

        self.playMusic = vlc.MediaPlayer(self.pathChoice)
        self.pausePlayIcon = 'I I'
        self.noteIconLabel.config(fg ='cyan4')
        self.barLine0.config(bg = 'cyan')
        self.barLine1.config(bg = 'cyan')
        self.pauseAndPlayButton.config(text = self.pausePlayIcon, font = ('impact',13))
        self.pauseAndPlayButton.place(x = 282, y = -3)
        self.playMusic.play()

    def Playm(self, event):
        self.ind = self.musicListBox.index(ACTIVE)
        self.musicListBox.bind('<Double-Button-1>',self.Stopm)
        self.proceedPlay()

    def Stopm(self,event):
        self.ind = self.musicListBox.index(ACTIVE)
        self.musicListBox.bind('<Double-Button-1>',self.Playm)
        self.playMusic.stop()
        self.proceedPlay()

    def Nextbtn(self):
        self.ind += 1
        self.musicListBox.selection_clear(0, END)
        self.musicListBox.selection_set(self.ind)
        self.musicListBox.activate(self.ind)
        self.playMusic.stop()
        if self.ind == len(self.MUSICLIST):
            self.ind = 0
            self.musicListBox.selection_set(0)
            self.musicListBox.selection_set(0)
            self.musicListBox.activate(0)
        self.proceedPlay()

    def Prevbtn(self):
        self.ind -= 1
        self.musicListBox.selection_clear(0, END)
        self.musicListBox.selection_set(self.ind)
        self.musicListBox.activate(self.ind)
        self.playMusic.stop()
        if self.ind == -1:
            self.ind += len(self.MUSICLIST)
            self.musicListBox.selection_clear(0, END)
            self.musicListBox.selection_set(self.ind)
            self.musicListBox.activate(self.ind)
        self.proceedPlay()
        
    def pseply(self):
        if self.pausePlayIcon == '▶':
            self.pausePlayIcon = 'I I'
            self.pauseAndPlayButton.config(text = self.pausePlayIcon, font = ('impact',13))
            self.pauseAndPlayButton.place(x = 282, y = -3)
            self.noteIconLabel.config(fg ='cyan4')
            self.barLine0.config(bg = 'cyan')
            self.barLine1.config(bg = 'cyan')
            self.playMusic.play()
        elif self.pausePlayIcon == 'I I':
            self.pausePlayIcon = '▶'
            self.pauseAndPlayButton.config(text = self.pausePlayIcon, font = ('impact',18))
            self.pauseAndPlayButton.place(x = 278, y = -12)
            self.noteIconLabel.config(fg = 'gray20')
            self.barLine0.config(bg = 'gray45')
            self.barLine1.config(bg = 'gray45')
            self.playMusic.pause()

    def stopPlay(self):
        self.tobedisabled = [self.pauseAndPlayButton,self.prevButton,self.nextButton]
        for y in self.tobedisabled:
            y.config(state = DISABLED)
        try:
            self.playMusic.stop()
        except:
            pass
        self.askdirctry() 

Player(root).place()

root.mainloop()
