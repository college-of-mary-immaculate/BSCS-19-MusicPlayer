import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Progressbar, Style
from threading import Thread
#import pygame
import time
import eyed3
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc

root = tk.Tk()
root.title("Music Player ♫")
root.geometry('508x470')
root.config(bg = 'gray25')
root.resizable(False,False)

class Player(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master = master
        self.ind = None
        self.PausePlayIcon = '▶'
        self.gui()

    def gui(self):
        self.volume = Scale(self.master, bd = 0, orient = VERTICAL, bg = 'gray20', length = 348, fg = 'cyan',
                            width = 60,activebackground = 'gray45', borderwidth = 0,troughcolor = 'gray25',
                            highlightbackground = 'gray45', from_ = 100, to = 0, font = ('calibri',10))

        self.volume.place(x = -2, y = 10)
        self.MListframe = Frame(self.master, height = 374, width = 420, borderwidth = 0, bg = 'gray20')
        self.MListframe.place(x = 94, y = 0)

        self.dirframe = Frame(self.MListframe, height = 30, width = 405, bg = 'gray45', borderwidth = 0)
        self.dirframe.place(x = 10, y = 10)

        self.foldr = Button(self.dirframe, text = '🗀', font = ('impact', 20), fg = 'white', bg = 'gray45',
                            activeforeground = 'cyan', activebackground = 'gray45', borderwidth = 0,command = self.askdirctry)
        self.foldr.place(x = 1, y = -17)

        self.fldrnme = Label(self.dirframe, text = '← Choose a folder to look for .mp3 and .wav files.',font =('calibri',8), fg = 'white', bg = 'gray45')
        self.fldrnme.place(x = 40, y = 6)

        self.lbframe = Frame(self.MListframe, borderwidth = 0, height = 500, width = 360, bg = 'gray')
        self.lbframe.place(x= 10, y = 40)

        self.sb = Scrollbar(self.lbframe, orient = VERTICAL,bg = 'gray5')
        self.sb.pack(side = 'right', fill = 'y')

        self.mlist = Listbox(self.lbframe,fg = 'white',bg = 'gray15', font = ('calibri',10),highlightcolor  = 'gray15',
                             selectbackground = 'cyan4', height = 20,width = 55,bd = 0,yscrollcommand = self.sb.set)
        self.mlist.pack()

        self.sb.config(command = self.mlist.yview)

        self.nomusic = Label(self.MListframe, text = 'Please choose a folder first!', font =('calibri',12), fg = 'white', bg = 'gray15')
        self.nomusic.place(x = 108, y = 190)

        self.playFrame = Frame(self.master, height = 62, width = 508, bg = 'gray45',borderwidth = 0)
        self.playFrame.place(x = 0, y = 372)
        
        self.progressFrame = Frame(self.playFrame, borderwidth = 0, height = 27, width = 505,bg = 'gray45' )
        self.progressFrame.place(x = 0, y = 0)
        self.pl_time = Label(self.progressFrame, text = '00:00', fg = 'white',bg = 'gray45', font =('calibri',8))
        self.pl_time.place(x=97,y=3)
        self.tl_time = Label(self.progressFrame, text = '00:00', fg = 'white',bg = 'gray45', font =('calibri',8))
        self.tl_time.place(x=471,y=3)
        self.pbar = Frame(self.progressFrame,borderwidth = 0, height = 2, width = 331, bg = 'gray60')
        self.pbar.place(x = 134, y = 11)
        self.thme = Style()
        self.thme.theme_use('clam')
        self.thme.configure("cyanpbar.Horizontal.TProgressbar", troughcolor = 'gray50', background = 'cyan', bordercolor = 'gray50',
                            lightcolor = 'cyan',darkcolor = 'cyan', borderwidth = 0)
        self.pbarr = Progressbar(self.pbar,style = "cyanpbar.Horizontal.TProgressbar", length = 331, mode = 'determinate')
        self.pbarr.place(x = 0, y = 0)

        self.current_songFrame = Frame(self.playFrame, borderwidth = 0, height = 42, width = 508,bg = 'gray45' )
        self.current_songFrame.place(x = 0, y = 20)
        self.Artist = Label(self.current_songFrame, text = 'Artist', font = ('calibri',10,), fg = 'white', bg = 'gray45')
        self.Artist.place(x = 97, y = 18)
        self.Songname = Label(self.current_songFrame, text = 'Song Name or File Name', font = ('calibri',12,'bold'), fg = 'white', bg = 'gray45')
        self.Songname.place(x = 97, y = -3)

        self.MPbuttonsFrame = Frame(self.master, height = 28, width = 508, bg = 'gray15')
        self.MPbuttonsFrame.place(x = 0, y = 438)

        self.pauseplayb = Button(self.MPbuttonsFrame, text = self.PausePlayIcon, font = ('impact',18),fg = 'white', bg = 'gray15',state = DISABLED,
                           activeforeground = 'cyan4',activebackground = 'gray15',borderwidth = 0, command = self.pseply)
        self.pauseplayb.place(x = 278, y = -12)

        self.prevb= Button(self.MPbuttonsFrame, text = '<', font = ('impact',17),fg = 'white', bg = 'gray15',state = DISABLED,
                           activeforeground = 'cyan4',activebackground = 'gray15',borderwidth = 0, command = self.Prevbtn)
        self.prevb.place(x = 248, y = -8)

        self.nextb= Button(self.MPbuttonsFrame, text = '>', font = ('impact',17),fg = 'white', bg = 'gray15',state = DISABLED,
                           activeforeground = 'cyan4',activebackground = 'gray15',borderwidth = 0, command = self.Nextbtn)
        self.nextb.place(x = 314, y = -8)

        self.MusicNoteFrame = Frame(self.master, height = 94, width = 94,borderwidth = 0)
        self.MusicNoteFrame.place(x = 0, y = 372)

        self.music = Label(self.MusicNoteFrame, text = '♫',fg = 'gray20', font = ('impact',40))
        self.music.place(x = 22, y = 8)

        self.mus = Label(self.dirframe, text = "♫:", font = ('calibri',10), bg = 'gray45')
        self.mus.place(x = 350, y = 4)

        self.musicount = Label(self.dirframe, text = '0', font = ('calibri', 8), bg = 'gray45', fg = 'white')
        self.musicount.place(x = 365, y = 6)

    def askdirctry(self):
        self.MUSICLIST = list()
        self.music.config(fg = 'gray20')
        self.foldr.config(command = self.stopPlay)
        self.mlist.delete(0,tk.END)
        self.nomusic.place(x = 108, y = 190)
        self.folderop = filedialog.askdirectory()

        if not self.folderop:
            self.mlist.unbind('<Double-Button-1>')
            self.foldr.config(fg = 'white')
            self.fldrnme.config(text = '← Choose a folder to look for .mp3 and .wav files.')
            self.nomusic.config(text = 'Please choose a folder first!')
            self.musicount.config(text = '0', fg = 'white')
            self.tobedisabled = [self.pauseplayb,self.prevb,self.nextb]
            for y in self.tobedisabled:
                y.config(state = DISABLED)
        else:
            if len(self.folderop) > 55:
                self.fldrnme.config(text = '← ' + self.folderop[0:55]+'...')
            else:
                self.fldrnme.config(text = '← ' + self.folderop)

            for x in os.listdir(self.folderop):
                if x.endswith('.mp3') or x.endswith('.wav'):
                    self.mlist.bind('<Double-Button-1>', self.Playm)
                    self.MUSICLIST.append(x)
                    self.foldr.config(command = self.stopPlay)
                    self.foldr.config(fg ='cyan')
                    self.nomusic.place_forget()
                    self.mlist.insert(END, "   ♪  {0}".format(x))
                    self.mlist.config()
                else:
                    self.mlist.unbind('<Double-Button-1>')
                    self.foldr.config(fg = 'white')
                    self.nomusic.config(text = 'No songs found in this folder')
                    self.tobedisabled = [self.pauseplayb,self.prevb,self.nextb]
                    for y in self.tobedisabled:
                        y.config(state = DISABLED)
            self.countsm = len(self.MUSICLIST)
            if self.countsm > 999:
                self.countsm = ('{0}+'.format(len(self.MUSICLIST)))
                self.musicount.config(text = self.countsm, fg = 'cyan')
            elif self.countsm == 0:
                self.musicount.config(text = self.countsm, fg = 'white')
            else:
                self.musicount.config(text = self.countsm, fg = 'cyan')

    def proceedPlay(self):
        self.mlist.bind('<Double-Button-1>', self.Stopm)
        self.tobeenabled = [self.pauseplayb, self.prevb,self.nextb]
        for x in self.tobeenabled:
            x.config(state = NORMAL)
        self.fchoice = self.MUSICLIST[self.ind]
        self.pathy = ("{0}\{1}".format(self.folderop,self.fchoice))
        
        self.MUSIC = eyed3.load(self.pathy)
        try:
            self.songTitle = self.MUSIC.tag.title
            if self.songTitle == None:
                if len(self.fchoice) > 50:
                    self.songTitle = ("{0}...".format(self.fchoice[:50]))
                else:
                    self.songTitle = self.fchoice
                self.Artist.config(text = 'Song File')
            else:
                try:
                    self.songArtist = self.MUSIC.tag.artist
                    if self.songArtist == None:
                        self.songArtist = 'No Artist'
                    self.Artist.config(text = self.songArtist)
                except AttributeError:
                    self.Artist.config(text = 'Song File')
            if len(self.songTitle) > 50:
                self.songTitle = ("{0}...".format(self.songTitle[:50]))
            else:
                pass
            self.Songname.config(text = self.songTitle)
        except AttributeError:
            self.Songname.config(text = self.fchoice)

        self.duration = self.MUSIC.info.time_secs
        self.mins, self.secs = divmod(self.duration,60)
        self.mins = round(self.mins)
        self.secs = round(self.secs)
        print(self.mins, self.secs)
        self.timeplay = ("{:02d}:{:02d}".format(self.mins,self.secs))
        self.tl_time.config(text = self.timeplay)

        self.playMusic = vlc.MediaPlayer(self.pathy)
        self.PausePlayIcon = 'I I'
        self.music.config(fg ='cyan4')
        self.pauseplayb.config(text = self.PausePlayIcon, font = ('impact',13))
        self.pauseplayb.place(x = 282, y = -3)
        self.playMusic.play()
        self.bar()

    def Playm(self, event):
        self.ind = self.mlist.index(ACTIVE)
        self.mlist.bind('<Double-Button-1>',self.Stopm)
        Thread(target = self.proceedPlay).start()
        Thread(target = self.bar).start()

    def Stopm(self,event):
        self.ind = self.mlist.index(ACTIVE)
        self.mlist.bind('<Double-Button-1>',self.Playm)
        self.playMusic.stop()
        Thread(target = self.proceedPlay).start()
        Thread(target = self.bar).start()

    def Nextbtn(self):
        self.ind += 1
        self.mlist.selection_clear(0, END)
        self.mlist.selection_set(self.ind)
        self.mlist.activate(self.ind)
        self.playMusic.stop()
        if self.ind == len(self.MUSICLIST):
            self.ind = 0
            self.mlist.selection_set(0)
            self.mlist.selection_set(0)
            self.mlist.activate(0)
        Thread(target = self.proceedPlay).start()
        Thread(target = self.bar).start()

    def Prevbtn(self):
        self.ind -= 1
        self.mlist.selection_clear(0, END)
        self.mlist.selection_set(self.ind)
        self.mlist.activate(self.ind)
        self.playMusic.stop()
        if self.ind == -1:
            self.ind += len(self.MUSICLIST)
            self.mlist.selection_clear(0, END)
            self.mlist.selection_set(self.ind)
            self.mlist.activate(self.ind)
        Thread(target = self.proceedPlay).start()
        Thread(target = self.bar).start()
        
    def pseply(self):
        if self.PausePlayIcon == '▶':
            self.PausePlayIcon = 'I I'
            self.pauseplayb.config(text = self.PausePlayIcon, font = ('impact',13))
            self.pauseplayb.place(x = 282, y = -3)
            self.music.config(fg ='cyan4')
            self.playMusic.play()
        elif self.PausePlayIcon == 'I I':
            self.PausePlayIcon = '▶'
            self.pauseplayb.config(text = self.PausePlayIcon, font = ('impact',18))
            self.pauseplayb.place(x = 278, y = -12)
            self.music.config(fg = 'gray20')
            self.playMusic.pause()

    def stopPlay(self):
        self.tobedisabled = [self.pauseplayb,self.prevb,self.nextb]
        for y in self.tobedisabled:
            y.config(state = DISABLED)
        try:
            self.playMusic.stop()
        except:
            pass
        self.askdirctry()
    
    def bar(self):

        self.m = 0
        self.s = -1
        self.timePlay = ''
        while self.timePlay != self.timeplay:
            if self.s == 59:
                self.s = -1
                self.m += 1
            self.s += 1
            self.timePlay += ("{:02d}:{:02d}".format(self.m,self.s))
            self.pl_time.place_forget()
            self.pl_time.config(text = self.timePlay)
            self.pl_time.place(x=97,y=3)
            self.timePlay = ''
            time.sleep(1)
  
        for i in range(0,101,1):
            self.pbarr['value'] = i
            self.master.update_idletasks()
            time.sleep(1)

            self.pbarr.pack(side = LEFT, fill = X, padx = 0)
        
    

Player(root).place()

root.mainloop()
