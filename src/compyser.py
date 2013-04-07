# -*- coding: utf8 -*-
# Dan Schlosser

import time
import wx
from wx.lib import intctrl
from functools import reduce
import random 
import pygame
import pygame.midi as midi
from pygame.locals import * #@UnusedWildImport
from pygame.midi import Input, Output

class Compyser(wx.Frame):
    """"""
    DEFUALT_WINDOW_SIZE = (500, 300)
    MAJOR_SCALE = [0,2,4,5,7,9,11]
    MINOR_SCALE = [0,2,3,5,7,8,10]
    RHYTHMS = [[4],[2],[1],[.5,.5],[.5],[1.5,.5],[1.5],[.25,.25],[.75,.25],
               [.25],[.34,.33,.33],[1.75,.25],[.67,.67,.66],
               [.125,.125,.125,.125,.125,.125,.125,.125],[.125,.125,.125,.125],
               [.2,.2,.2,.2,.2],[.4,.4,.4,.4,.4]]
    RHYTHM_DIVIDERS = [2,3,4,6,7,9,12,13,15,17]
    MAJ_NOTES = [0,7,4,2,9,11,5,10,6,8,3,1]
    MIN_NOTES = [0,7,3,2,8,10,11,5,6,1,9,4]
    NOTE_DIVIDERS = [2,3,5,6,7,8,9,10,11,12]
    MAJ_CHORDS = [{"name":"I",          "type":0,"notes":[0,4,7],           "tendency":[]},                         #0
                  {"name":"V",          "type":2,"notes":[7,11,14],         "tendency":[]},
                  #----
                  {"name":"IV",         "type":1,"notes":[5,8,12],          "tendency":[]},
                  {"name":"ii",         "type":1,"notes":[2,5,8],           "tendency":[]},
                  #----
                  {"name":"vi",         "type":1,"notes":[9,12,16],         "tendency":[]},
                  {"name":"V7",         "type":2,"notes":[7,11,14,17],      "tendency":[]},                         #5
                  {"name":"vii(dim)",   "type":2,"notes":[11,14,17],        "tendency":[]},
                  #----
                  {"name":"ii(7)",      "type":1,"notes":[2,5,9,12],        "tendency":[]},
                  {"name":"I(6)",       "type":0,"notes":[0,4,7,9],         "tendency":[]},
                  #----
                  {"name":"I(M7)",      "type":0,"notes":[0,4,7,11],        "tendency":[]},
                  {"name":"I(M9)",      "type":0,"notes":[0,4,7,11,14],     "tendency":[]},                         #10
                  {"name":"V(9)",       "type":2,"notes":[7,11,14,17,21],   "tendency":[]},
                  {"name":"vii(dim7)",  "type":2,"notes":[11,14,17,20],     "tendency":[]},
                  #----
                  {"name":"IV(7)",      "type":1,"notes":[5,9,12,16],       "tendency":[]},
                  {"name":"vi(7)",      "type":1,"notes":[9,12,16,19],      "tendency":[]},
                  #----
                  {"name":"iii",        "type":1,"notes":[4,7,11],          "tendency":[2,3,4,7,13,14,20,21,22]},   #15
                  {"name":"iii(7)",     "type":1,"notes":[4,7,11,14],       "tendency":[2,3,4,7,13,14,20,21,22]},
                  {"name":"V(7)/V",     "type":3,"notes":[2,6,9,12],        "tendency":[1,5,6,11,12,18,19,25,26,27]},
                  {"name":"V(7b9)",     "type":2,"notes":[7,11,14,17,20],   "tendency":[]},
                  {"name":"V(13)",      "type":2,"notes":[7,11,14,17,21,28],"tendency":[]},
                  #----
                  {"name":"V(7)/ii",    "type":3,"notes":[9,13,16,19],      "tendency":[3,7]},                         #20
                  {"name":"bII(dim)",   "type":3,"notes":[1,4,7],           "tendency":[3,7]},
                  {"name":"bII(dim7)",  "type":3,"notes":[1,4,7,10],        "tendency":[2,3,6,7,12,13]},
                  {"name":"#IV(dim)",   "type":3,"notes":[6,9,12],          "tendency":[1,5,6,11,12,18,19,25,26,27]},
                  {"name":"#IV(dim7)",  "type":3,"notes":[6,9,12,15],       "tendency":[1,5,6,11,12,15,16,18,19,25,26,27,28]},
                  #----
                  {"name":"V(7#9)",     "type":2,"notes":[7,11,14,17,22],   "tendency":[]},                         #25
                  {"name":"V(7b13)",    "type":2,"notes":[7,11,14,17,20,27],"tendency":[]},
                  {"name":"V(7#11)",    "type":2,"notes":[7,11,14,17,25],   "tendency":[]},
                  #----
                  {"name":"bII(M7)",    "type":0,"notes":[1,5,8,12],        "tendency":[0,8,9,10]}, 
                  ]
    MAJ_CHORD_DIVIDERS = [2,4,7,9,13,15,20,25,28,29]
    MIN_CHORDS = [{"name":"i",          "type":0,"notes":[0,3,7],           "tendency":[]},                         #0
                  {"name":"v",          "type":2,"notes":[7,10,14],         "tendency":[]},
                  #----
                  {"name":"iv",         "type":1,"notes":[5,8,12],          "tendency":[]},
                  {"name":"ii(0)",      "type":1,"notes":[2,5,7],           "tendency":[]},
                  #----
                  {"name":"VI",         "type":1,"notes":[10,12,15],        "tendency":[]},
                  {"name":"V",          "type":2,"notes":[7,11,14],         "tendency":[]},                         #5
                  {"name":"V7",         "type":2,"notes":[7,11,14,17],      "tendency":[]},                         
                  {"name":"vii(dim)",   "type":2,"notes":[11,14,17],        "tendency":[0,10,11,12]},
                  {"name":"VII",        "type":1,"notes":[10,14,17],        "tendency":[]},
                  #----
                  {"name":"ii(m7b5)",   "type":1,"notes":[2,5,8,12],        "tendency":[]},
                  {"name":"i(6)",       "type":0,"notes":[0,3,7,9],         "tendency":[]},                         #10
                  #----
                  {"name":"i(M7)",      "type":0,"notes":[0,3,7,11],        "tendency":[]},
                  {"name":"i(M9)",      "type":0,"notes":[0,3,7,11,14],     "tendency":[]},                         
                  {"name":"V(9)",       "type":2,"notes":[7,11,14,17,21],   "tendency":[]},
                  {"name":"VII(7)",     "type":1,"notes":[10,14,17,20],     "tendency":[]},
                  {"name":"vii(dim7)",  "type":2,"notes":[11,14,17,20],     "tendency":[0,10,11,12,18,19,25,26]},   #15
                  #----
                  {"name":"iv(7)",      "type":1,"notes":[5,8,12,16],       "tendency":[]},
                  {"name":"VI(7)",      "type":1,"notes":[8,12,15,19],      "tendency":[]},
                  #----
                  {"name":"III",        "type":1,"notes":[3,7,10],          "tendency":[]},   
                  {"name":"III(7)",     "type":1,"notes":[3,7,10,14],       "tendency":[]},
                  {"name":"V(7)/V",     "type":3,"notes":[2,6,9,12],        "tendency":[1,5,6,13,21,27,28,29]},#20
                  {"name":"V(7b9)",     "type":2,"notes":[7,11,14,17,20],   "tendency":[]},
                  #----
                  {"name":"V(7)/ii",    "type":3,"notes":[9,13,16,19],      "tendency":[3,9]},                         
                  {"name":"bII(dim)",   "type":3,"notes":[1,4,7],           "tendency":[3,9]},
                  {"name":"bII(dim7)",  "type":3,"notes":[1,4,7,10],        "tendency":[2,3,4,7,9,15,16,17]},
                  {"name":"#IV(dim)",   "type":3,"notes":[6,9,12],          "tendency":[1,5,6,13,21,27,28,29]},#25
                  {"name":"#IV(dim7)",  "type":3,"notes":[6,9,12,15],       "tendency":[1,5,6,8,13,14,21,27,28,29,30]},
                  #----
                  {"name":"V(7#9)",     "type":2,"notes":[7,11,14,17,22],   "tendency":[]},                         
                  {"name":"V(7b13)",    "type":2,"notes":[7,11,14,17,20,27],"tendency":[]},
                  {"name":"V(7#11)",    "type":2,"notes":[7,11,14,17,25],   "tendency":[]},
                  #----
                  {"name":"bII(M7)",    "type":0,"notes":[1,5,8,12],        "tendency":[0,10,11,12]},                 #30
                  ]
    MIN_CHORD_DIVIDERS = [2,4,9,11,16,18,22,27,30,31]
    
    
    
    def __init__(self, parent, size=DEFUALT_WINDOW_SIZE):
        """"""
        wx.Frame.__init__(self,parent, size=size)
#        midex.input_main(1)
        
        #--Font Setup----------------------------------------------------------
        self.font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        self.consoleFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        self.SetFont(self.font)
        
        #--Values--------------------------------------------------------------
        self.notes = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        self.tune = []
        self.final = 0
        self.isMajor = True
        self.key = "A Major"
        self.scale = []
        
        #--Widgets-------------------------------------------------------------
        self.mainPanel = wx.Panel(self)
        
        self.keys = [k+" Major" for k in self.notes]
        self.keys += [k+" Minor" for k in self.notes]
        self.keyPicker = wx.ComboBox(self.mainPanel, style=wx.CB_READONLY, 
                                     value = "A Major", choices=self.keys)
        
        self.recordButton = wx.Button(self.mainPanel, label="&Record")
        self.playButton = wx.Button(self.mainPanel, label="&Play")
        self.playButton.Disable()
        
        self.rhyText = wx.StaticText(self.mainPanel, label="Rhythmic Complexity:")
        self.melText = wx.StaticText(self.mainPanel, label="Melodic Complexity:")
        self.harmText = wx.StaticText(self.mainPanel, label="Harmonic Complexity:")
        
        self.rhyBox = intctrl.IntCtrl(self.mainPanel, size=(50,-1), value=1, min=1, max=10, 
                                      limited=True,)
        self.melBox = intctrl.IntCtrl(self.mainPanel, size=(50,-1), value=1, min=1, max=10, 
                                      limited=True,)
        self.harmBox = intctrl.IntCtrl(self.mainPanel, size=(50,-1), value=1, min=1, max=10, 
                                      limited=True,)
        
        self.console = wx.TextCtrl(self.mainPanel, style= wx.TE_MULTILINE | wx.SUNKEN_BORDER)
        self.console.SetFont(self.consoleFont)
                
        #--Status Bar----------------------------------------------------------
        
        self.CreateStatusBar()
        
        #--Sizers--------------------------------------------------------------
        self.textSizer = wx.BoxSizer(wx.VERTICAL)
        self.textSizer.AddStretchSpacer(1)
        self.textSizer.Add(self.rhyText, 0, wx.ALIGN_RIGHT|wx.LEFT, border=5)
        self.textSizer.AddStretchSpacer(1)
        self.textSizer.Add(self.melText, 0, wx.ALIGN_RIGHT|wx.LEFT, border=5)
        self.textSizer.AddStretchSpacer(1)
        self.textSizer.Add(self.harmText, 0, wx.ALIGN_RIGHT|wx.LEFT, border=5)
        self.textSizer.AddStretchSpacer(1)
        
        self.intSizer = wx.BoxSizer(wx.VERTICAL)
        self.intSizer.AddStretchSpacer(1)
        self.intSizer.Add(self.rhyBox, 0)
        self.intSizer.AddStretchSpacer(1)
        self.intSizer.Add(self.melBox, 0)
        self.intSizer.AddStretchSpacer(1)
        self.intSizer.Add(self.harmBox, 0)
        self.intSizer.AddStretchSpacer(1)
        
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftSizer.AddStretchSpacer(1)
        self.leftSizer.Add(self.keyPicker, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.leftSizer.Add(self.recordButton, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.leftSizer.Add(self.playButton, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.leftSizer.AddStretchSpacer(1)
        
        self.rightSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rightSizer.Add(self.textSizer, 1, wx.EXPAND)
        self.rightSizer.Add(self.intSizer, 0)
        
        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.topSizer.Add(self.leftSizer, 1)
        self.topSizer.Add(self.rightSizer, 1)
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.topSizer,1,wx.EXPAND|wx.ALL, border=10)
        self.mainSizer.Add(self.console, 1,wx.EXPAND | wx.LEFT | wx.BOTTOM | 
                           wx.RIGHT, border=10)
        self.mainPanel.SetSizerAndFit(self.mainSizer)
        
        #--Setup -------------------------------------------------------
        
        midi.init()
        pygame.init()
        pygame.fastevent.init()
        
        #--Event Binding-------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.onRecord, self.recordButton)
        
        #--Show----------------------------------------------------------------
        self.Show(True)   
        
        
    def write(self, msg):
        """"""
        self.console.AppendText(str(msg)+"\n")
        
    def processKey(self):
        """"""
        c2a = 9 
        self.key = self.keyPicker.GetValue()
        if self.key.endswith("Minor"):
            self.isMajor = False
        self.final = (self.notes.index(self.key.split(" ")[0])+c2a)%12
        self.scale = [deg + self.final for deg in (self.MAJOR_SCALE if 
                                                   self.isMajor else 
                                                   self.MINOR_SCALE)]
        self.write("We are in " +str(self.key)+ ".")
        self.write("The final is "+ str(self.final))
        self.write("The scale is "+str(self.scale))
        self.write("That's a " +("major" if self.isMajor else "minor")+ " scale!")
        
    def makeSong(self):
        """"""
        
    def makeRhythm(self):
        """"""
        plex = self.rhyBox.GetValue()-1
        #rhythms = reduce((lambda x,y: x+y), self.RHYTHMS[:self.RHYTHM_DIVIDERS[plex]])
        rhythms = self.RHYTHMS[:self.RHYTHM_DIVIDERS[plex]]
        beat = []
        total = 0
        while total <4:
            rhyth = rhythms[random.randint(range(len(rhythms)))]
            if total + sum(rhyth) <=4:
                for note in rhyth:
                    if random.random()<.3:
                        
    
    def onRecord(self, e):
        """"""
        if self.recordButton.GetLabel()=="&Stop":
            self.recordButton.SetLabel("&Record")
            self.recordButton.Disable()
            self.going = False
            self.makeSong()
        else:
            if self.recordButton.GetLabel()=="&Record":
                self.recordButton.SetLabel("&Stop")
            midiIn = Input(midi.get_default_input_id())
            
            self.processKey()
            
            self.write( "Getting input from:")
            self.write( midi.get_device_info(midi.get_default_input_id()))
            
            event_get = pygame.fastevent.get
            event_post = pygame.fastevent.post
            self.going = True
            startTime = time.time()
            try:
                while self.going and (time.time()-startTime)<=20:
                    events = event_get()
                    for e in events:
                        if e.type in [QUIT]:
                            self.going = False
                    if midiIn.poll():
                        midiEvents = midiIn.read(10)
#                        self.write( midiEvents)
                        for m in midiEvents:
                            if m[0][1] > 0 and m[0][2]>0:
                                self.write("Read note:" + str(self.notes[(m[0][1]+3)%12]))
                                self.tune.append(m[0][1])
                        midiEvs = midi.midis2events(midiEvents,
                                                    midiIn.device_id)
                        for mE in midiEvs:
#                            self.write( "mE = ", mE)
                            event_post(mE)
            finally:
                del midiIn
                midi.quit()

class chord(Object):
    
    def __init__(self,notes,): 
    
    
if __name__ == '__main__': 
    app = wx.App(False)
    panel = Compyser(None)
    app.MainLoop()
