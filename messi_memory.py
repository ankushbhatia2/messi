#-------------------------------------------------------------------------------
# Name:        Messi
# Purpose:     Virtual Personal assistant
#
# Author:      Ankush
#
# Created:     11-06-2015
# Copyright:   (c) Batman 2015
# Licence:     Standard DC License
#-------------------------------------------------------------------------------

#Module imports
import pyttsx                  #Text to speech
from socket import gethostname #To get the machine name
from bs4 import BeautifulSoup  #Scraper
import requests, urllib, json  #for request handling and api
import wx                      #GUI
import cv2                     #Camera

#Global objects
app = wx.App()
engine = pyttsx.init()


#Global String
ask = ''

#Memory of bot
class messi_memory:
    _end = '__end__'
    root = dict()
    def __init__(self, word):
        current_node = self.root
        for letter in word:
            current_node = current_node.setdefault(letter, {})
        current_node[self._end] = self._end
    def insert(self, word):
        current_node = self.root
        for letter in word:
            if letter in current_node:
                current_node = current_node[letter]
            else:
                current_node = current_node.setdefault(letter, {})
        current_node = current_node.setdefault(self._end, self._end)
    def search(self, word):
        current_node = self.root
        for letter in word:
            if letter in current_node:
                current_node = current_node[letter]
            else:
                return False
        else:
            if self._end in current_node:
                return True
            else:
                return False
    def assign(self, word, function='', speak=''):
        current_node = self.root
        for letter in word:
            if letter in current_node:
                current_node = current_node[letter]
        current_node['do'] = function
        current_node['speak'] = speak
    def get_function(self, word):
        current_node = self.root
        for letter in word:
            if letter in current_node:
                current_node = current_node[letter]
        return current_node['do'], current_node['speak']

#Global Object
m = messi_memory('Messi')           #Memory

#Scraping
def scraper(url):
    try:
        result = ''
        url = url.lower()
        url = url.replace(' ', '+')
        r  = requests.get('https://www.google.co.in/search?q='+url+'&oq='+url+'&aqs=chrome..69i57j0l5.718j0j7&sourceid=chrome&es_sm=93&ie=UTF-8')
        data = r.text
        soup = BeautifulSoup(data)                                                 #Scraper
        print url
        print 'Search Results'
        for i in soup.findAll('a'):
            if i.parent.name == 'h3':
                p = str(i)
                result+=p[p.index('>')+1:p.index('</a>')].replace('<b>', '').replace('</b>', '')
                result+='\n'
        url = url.replace('+', '_')
        a = requests.get('https://www.wikipedia.org/wiki/'+url)
        data = a.text
        soup = BeautifulSoup(data)
        p = list(str(soup.find('p')))
        i = 0
        r = len(p)
        while i < r:
            if p[i] == '<':
                while p[i] != '>':
                    p[i] = ''
                    i+=1
                p[i] = ''
            if p[i] == '[':
                while p[i] != ']':
                    p[i] = ''
                    i+=1
                p[i] = ''
            i+=1
        p = ''.join(p)
        print p
        m.insert(url.replace('_', ' '))
        m.assign(url.replace('_', ' '), '', p)
        print m.root
        return result
    except:
        #engine.say('Sorry, I can\'t connect to the internet right now. Till then. Hail Bayern Munich')
        #engine.runAndWait()
        return 'Sorry, I can\'t connect to the internet right now. Till then. Hail Bayern Munich'

#Function for initialization of messi's memory
def assign_memory():
    m.insert('football')
    m.assign('football', 'I love football')
    m.insert('foot')
    m.assign('foot', 'Foot')
    m.insert('chintu')

#Function for reply
def doit(asked):
    if m.search(asked.lower()):
        print m.get_function(asked.lower())
        return m.get_function(asked.lower())
    else:
        asked = asked.replace('what ', '')
        asked = asked.replace('is ', '')
        asked = asked.replace('why ', '')
        asked = asked.replace('how ', '')
        return ('', scraper(asked))

#GUI
class GUI(wx.Frame):
    APP_EXIT = 1
    def __init__(self, parent, title):
        super(GUI, self).__init__(parent, title=title,
            size=(500, 600))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        self.panel = wx.Panel(self, -1)
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()
        qmi = wx.MenuItem(fileMenu, self.APP_EXIT, '&Quit\tCtrl+Q')
        fileMenu.AppendItem(qmi)

        self.Bind(wx.EVT_MENU, self.OnQuit, id=self.APP_EXIT)
        self.shst = viewMenu.Append(wx.ID_ANY, 'Show statubar',
            'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shtl = viewMenu.Append(wx.ID_ANY, 'Show toolbar',
            'Show Toolbar', kind=wx.ITEM_CHECK)

        viewMenu.Check(self.shst.GetId(), True)
        viewMenu.Check(self.shtl.GetId(), True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)


        menubar.Append(fileMenu, '&File')
        menubar.Append(viewMenu, '&View')
        self.SetMenuBar(menubar)

        text2=wx.StaticText(self.panel, label='Hello '+gethostname(), pos=(0, 0), style=wx.ALIGN_RIGHT)
        text2.SetForegroundColour((255,255,255))
        text3=wx.StaticText(self.panel, label="I'm Messi, your personal assistant", pos=(0, 20), style=wx.ALIGN_RIGHT)
        text3.SetForegroundColour((255,255,255))
        text4=wx.StaticText(self.panel, label='To know my functionalities, try saying, Hello Messi', pos=(0, 40), style=wx.ALIGN_RIGHT)
        text4.SetForegroundColour((255,255,255))


        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')
        self.textCtrl = wx.TextCtrl(self.panel, pos=(0, 495), size=(400, 20))
        self.panel.SetBackgroundColour('#000000')
        cbtn = wx.Button(self.panel, label='Enter', pos=(410, 495), size=(70, 20))

        cbtn.Bind(wx.EVT_BUTTON, self.OnEnter)
    def ToggleStatusBar(self, e):

        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, e):

        if self.shtl.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

    def OnQuit(self, e):
        self.Close()

    def OnEnter(self, e):
        ask = str(self.textCtrl.GetValue())
        text=wx.StaticText(self.panel, label='', pos=(0, 0), style=wx.ALIGN_LEFT)
        text.SetLabel(gethostname()+": "+ask)
        text.SetForegroundColour((255,255,255))
        get = doit(ask)
        print get
        get_do = ''
        if get[0] != '':
            get_do = get[0]
        get_speak = get[1]
        if get_speak != '':
            text1=wx.StaticText(self.panel, pos=(0, 20), label='', style=wx.ALIGN_LEFT)
            text1.SetLabel("Messi: "+ get_speak)
            text1.SetForegroundColour((255,255,255))
            if '\n' in get_speak:
                engine.say('I found the following search results')
                engine.runAndWait()
            else:
                engine.say(get_speak)
                engine.runAndWait()
        if get_do != '':
            eval(get_do)
        text.Destroy()
#Global object
GUI(None, title='Messi')            #GUI

#main
if __name__ == '__main__':
    engine.say('Hello '+gethostname())
    engine.say("I'm Messi, your personal assistant")
    engine.say('To know my functionalities, try saying, Hello Messi')
    engine.runAndWait()
    assign_memory()
    print m.root

app.MainLoop()