#-------------------------------------------------------------------------------
# Name:        Messi
# Purpose:     Virtual Personal assistant
#
# Author:      Ankush
#
# Created:     11-06-2015
# Copyright:   (c) Batman 2015
# Licence:
#-------------------------------------------------------------------------------


#Module imports
import pyttsx                  #Text to speech
from socket import gethostname #To get the machine name
from bs4 import BeautifulSoup  #Scraper
import requests, urllib, json  #for request handling and api
import cv2                     #Camera

#Global variables and objects
engine = pyttsx.init()
i = 0
#app = wx.App()

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

#Methods
def functionalities_fake():
    engine.say('I can do almost every virtual thing for you.')
    engine.say('Well, actually I am too lazy to describe my functionalities')
    engine.say('What can I say? I\'m just like my developer. A Lazy Swine')
    engine.say('I won\'t say it until you force me')
    engine.say('Try saying please messi')
    engine.runAndWait()
    global i
    i+=1

def functionalities():
    engine.say('I can do following things for you if you\'re worth it')
    engine.runAndWait()
    print 'Gotta write functionalities here'

def getWeather(city, country):
    try:
        url = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+(city[0].upper()+city[1:]+','+country[0].upper()+country[1:]))

        data = url.text
        data1 = json.loads(data)
        print 'City Name : ' + data1['name']
        print 'Country Name : ' + data1['sys']['country']
        print data
        #print 'Clouds : ' + data1['clouds']['all']
    except:
        engine.say('I\'m Sorry. I can\'t connect to the internet just like I can\'t connect to a Football game')
        engine.runAndWait()

def getIpLocation(Use):
    try:
        url = urllib.urlopen("http://bot.whatismyipaddress.com").read()
        url2 = urllib.urlopen("http://ip-api.com/json/"+url).read()
        data = json.loads(url2)
        if Use == True:
            return data['city'], data['country']
        else:
            return url, data
    except:
        engine.say('I\'m Sorry. I can\'t connect to the internet because Neuer is giving me nightmares')
        engine.runAndWait()

def getDirection(place_from, place_to):
    try:
        url = urllib.urlopen('https://maps.googleapis.com/maps/api/directions/json?origin='+place_from+'&destination='+place_to+'&key=AIzaSyCPrIT_X_1S7vhHANoCrcuRB7k432PL1Zo').read()
        data = json.loads(url)
        for i in data['routes'][0]['legs'][0]['steps']:
            print i['html_instructions'].strip('<b>').strip('</b>').strip('<div style="font-size:0.9em">').strip('</div>')
    except:
        engine.say('I\'m Sorry. I can\'t connect to the internet right now, or this place exists in your dreams. No offence.')
        engine.runAndWait()

def open_cam(gray_scale):
    try:
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        video_capture = cv2.VideoCapture(0)

        while True:
        # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Display the resulting frame
            if gray_scale == True:
                cv2.imshow('Video', gray)
            else:
                cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()
    except:
        engine.say('There are no cameras available or there is a problem with your camera')
        engine.say('Please get your cameras fixed or get a new one. You should see your face and hate yourself')
        engine.runAndWait()


def scraper(url):                   #Scraping
    try:
        url = url.replace(' ', '+')
        r  = requests.get('https://www.google.co.in/search?q='+url+'&oq='+url+'&aqs=chrome..69i57j0l5.718j0j7&sourceid=chrome&es_sm=93&ie=UTF-8')
        data = r.text
        soup = BeautifulSoup(data)
        print url
        print 'Search Results'
        for i in soup.findAll('a'):
            if i.parent.name == 'h3':
                p = str(i)
                print p[p.index('>')+1:p.index('</a>')].replace('<b>', '').replace('</b>', '')

        engine.say('I found the following search results')
        engine.runAndWait()
    except:
        engine.say('Sorry, I can\'t connect to the internet right now. Till then. Hail Bayern Munich')
        engine.runAndWait()

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
    def assign(self, word, function):
        current_node = self.root
        for letter in word:
            if letter in current_node:
                current_node = current_node[letter]
        current_node['function'] = function
    def get_function(self, word):
        current_node = self.root
        for letter in word:
            if letter in current_node:
                current_node = current_node[letter]
        return current_node['function']

#Main Function
def main():
    #frame = wx.Frame(None, -1, 'Messi')
    #frame.Show()

    engine.say('Hello '+gethostname())
    engine.say("I'm Messi, your personal assistant")
    engine.say('To know my functionalities, try saying, Hello Messi')
    engine.runAndWait()
    while True:
        url = str(raw_input('Write anything'))
        if 'goodbye' in url.lower() and 'messi' in url.lower():
            engine.say('GoodBye '+gethostname())
            engine.runAndWait()
            break
        elif url.lower() == 'please messi' and i%2 == 1:
            functionalities()
            global i
            i+=1
        elif url.lower() == 'please messi' and i%2 == 0:
            engine.say('Please What? You have to say Hello Messi first. I\'m a bloody attention seeker. Mwahahahahahaha')
            engine.say('F Y I That was an evil laugh')
            engine.runAndWait()
        elif 'open camera' in url.lower() or 'camera open' in url.lower():
            engine.say('Do you want camera in gray scale?')
            engine.runAndWait()
            ask = str(raw_input())
            if ask.lower() == 'yes':
                engine.say('Opening camera in gray scale')
                engine.runAndWait()
                open_cam(True)
            else:
                engine.say('Opening camera')
                engine.runAndWait()
                open_cam(False)
        elif 'what\'s up' in url.lower() or 'whats up' in url.lower():
            engine.say('Nothing much, just adoring Bayern Munich. You should do that too')
            engine.runAndWait()
        elif 'ronaldo' in url.lower():
            engine.say('Screw Ronaldo, Screw Messi, Reebery is the best')
            engine.runAndWait()
        elif 'knock knock' in url.lower():
            engine.say('Knock Knock. who\'s there. Messi. Messi who. Messi who can\'t even kick a ball. Damn! It hurts.')
            engine.runAndWait()
        elif 'hello' in url.lower() and 'messi' in url.lower():
            functionalities_fake()
        elif 'weather' in url.lower():
            engine.say('Weather of which city?(And please specify country\'s name too)')
            engine.say('Say current to get the weather report of current location')
            engine.runAndWait()
            loc = str(raw_input())
            if loc == 'current':
                try:
                    city, country = getIpLocation(True)
                    getWeather(city, country)
                except:
                    print 'Boy oh boy, Internen\'s down man. Can\'t help you nigga'
            else:
                get_both = loc.split()
                getWeather(get_both[0], get_both[1])
        elif 'get directions' in url.lower():
            engine.say('Please specify the source and destination locations again with city\'s name too')
            engine.runAndWait()
            loc11, loc12, loc21, loc22 = map(str, raw_input().split())
            engine.say('Getting Directions')
            engine.runAndWait()
            getDirection(loc11+','+loc12, loc21+','+loc22)
        elif 'i love you' in url.lower():
            engine.say('No. Don\'t love me. Love Bayern Munich. I love them too.')
            engine.runAndWait()
        else:
            scraper(url)
    #app.MainLoop()

if __name__ == '__main__':
    main()
