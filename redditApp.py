#requires [praw, PyQt5, _thread, sys, urllib, os, shutil]

import praw as praw
import PyQt5 as PyQt5
from PyQt5.QtWidgets import *
import _thread as thread
import sys as sys
import urllib as urllib
import os as os
import shutil as shutil

if ('tmp' not in os.listdir('.')):
    os.mkdir('tmp')

for item in os.listdir('./tmp'):
    os.remove('./tmp/{}'.format(item))

reddit_bot = praw.Reddit(user_agent = 'katznbot', client_id = '_CIuAjxI8TaKvg', client_secret = 'HnpYVUD2jouM--6OdFzdFNJ_g2E', username = 'katznbot', password = '')

application_running = True
application_ytop = 0

application = QApplication(sys.argv)

ut = ''

previousImages = []
previousLoadAmounts = {}
subreddit_current = 'aviation'

mainContentAreaWidth = 500
actualMCA = (mainContentAreaWidth + 30)
sidebarMinWidth = 300
consoleWidth = 200

window = QWidget()
window.setWindowTitle('PC reddit browser')
window.setMinimumSize((actualMCA + sidebarMinWidth + 1), 400)
window.setStyleSheet('QWidget{background-color:white;}')

scroll = QScrollArea(window)
scroll.setWidgetResizable(True)
scrollContent = QWidget(scroll)
scrollLayout = QVBoxLayout(scrollContent)
scrollContent.setLayout(scrollLayout)
scroll.setWidget(scrollContent)
scroll.resize(500, 500)

sidebarScroll = QScrollArea(window)
sidebarScroll.setWidgetResizable(True)
sidebarScrollContent = QWidget(sidebarScroll)
sidebarScrollLayout = QVBoxLayout(sidebarScrollContent)
sidebarScrollContent.setLayout(sidebarScrollLayout)
sidebarScroll.setWidget(sidebarScrollContent)
sidebarScroll.resize(500, 500)

gppsbs = '''
QPushButton{background-color:lightgray;border:1px solid black;color:black;font-family:Verdadna;font-size:15px;}
QPushButton:hover{background-color:white;border:1px solid black;color:black;font-family:Verdadna;font-size:15px;}
'''

sidebarScroll_attrb1 = QPushButton()
sidebarScroll_attrb1.setStyleSheet(gppsbs)
sidebarScroll_attrb1.setText('Load more images from this subreddit:')
sidebarScroll_attrb1.clicked.connect(lambda: utils.loadMore(5))
sidebarScrollLayout.addWidget(sidebarScroll_attrb1)

sidebarScroll_e1 = QPlainTextEdit()
sidebarScroll_e1.setFixedHeight(30)
sidebarScroll_e1.setPlainText(subreddit_current)
sidebarScroll_e1.setStyleSheet('QPlainTextEdit{background-color:white;color:black;font-family:Verdanda;font-size:15px;}')
sidebarScrollLayout.addWidget(sidebarScroll_e1)

sidebarScroll_attrb2 = QPushButton()
sidebarScroll_attrb2.setStyleSheet(gppsbs)
sidebarScroll_attrb2.setText('Clear images')
sidebarScroll_attrb2.clicked.connect(lambda: utils.clearMCD())
sidebarScrollLayout.addWidget(sidebarScroll_attrb2)

sidebarScroll_attrb2 = QPushButton()
sidebarScroll_attrb2.setStyleSheet(gppsbs)
sidebarScroll_attrb2.setText('EXIT')
sidebarScroll_attrb2.clicked.connect(lambda: exit())
sidebarScrollLayout.addWidget(sidebarScroll_attrb2)

console = QPlainTextEdit(window)
console.setStyleSheet('QPlainTextEdit{background-color:white;color:black;font-family:Courier New;font-size:13px;}')
console.move((actualMCA + sidebarMinWidth), 0)

class utils():
    def consolelog(string):
        global console
        string = str(string)
        console.setPlainText((console.toPlainText() + '\n\n' + string))
        console.verticalScrollBar().setValue(console.verticalScrollBar().maximum())
    def getImageDataUsingUrl(url):
        utils.consolelog('utils.getImageDataUsigUrl({})'.format(url))
        try:
            response = urllib.request.urlopen(url)
            imagefilename = str(url).split('/')[(url.count('/'))]
            imagefilename = imagefilename.split(':')[(imagefilename.count(':'))]
            image = open(('./tmp/' + imagefilename), 'wb')
            image.write(response.read())
            image.close()
            return imagefilename
        except Exception as err:
            print (err)
            return '.'
    def mkimage(imagename):
        utils.consolelog('utils.mkimage({})'.format(imagename))
        global window, application_ytop, scrollLayout
        pic = QLabel()
        pic.resize(300, 300)
        pixmap = PyQt5.QtGui.QPixmap('./tmp/{}'.format(imagename))
        try:
            img_aspect_ratio = (float(pixmap.size().width()) / pixmap.size().height())
        except:
            img_aspect_ratio = 1.8
        width = 450
        height = (450 / img_aspect_ratio)
        pixmap = pixmap.scaled(width, height)
        pic.setPixmap(pixmap)
        pic.resize(width, height + 15)
        pic.move(0, application_ytop)
        pic.setStyleSheet('QLabel{background-color:white;}')
        application_ytop += (height + 15)
        scrollLayout.addWidget(pic)
        vor = QLabel()
        vor.setStyleSheet('QLabel{background-color:white;color:black;text-align:left;font-size:15px;font-family:Verdana;border:none;}')
        vor.setText(ut)
        vor.setFixedWidth(mainContentAreaWidth) #works but doesnt word-wrap
        vor.setWordWrap(True)
        scrollLayout.addWidget(vor)
        postOptionsLayout = QWidget()
        lbss = '''
QPushButton{background-color:lightgray;color:black;border:1px solid black;font-family:Verdana;font-size:13px;margin:0px;}
QPushButton:hover{background-color:white;color:black;border:1px solid black;font-family:Verdana;font-size:13px;margin:0px;}
'''
        l1 = QHBoxLayout()
        l1_b1 = QPushButton()
        l1_b1.setText('Save')
        l1_b1.setStyleSheet(lbss)
        l1_b1.setFixedSize((mainContentAreaWidth / 3.5), 25)
        l1_b1.clicked.connect(lambda: utils.saveFile(imagename))
        l1.addWidget(l1_b1)
        l1_b2 = QPushButton()
        l1_b2.setText('View on reddit.com')
        l1_b2.setStyleSheet(lbss)
        l1_b2.setFixedSize((mainContentAreaWidth / 3.5), 25)
        l1_b2.clicked.connect(lambda: print('This function is a work in progress.'))
        l1.addWidget(l1_b2)
        l1_b3 = QPushButton()
        l1_b3.setText('Share')
        l1_b3.setStyleSheet(lbss)
        l1_b3.setFixedSize((mainContentAreaWidth / 3.5), 25)
        l1.addWidget(l1_b3)
        postOptionsLayout.setLayout(l1)
        scrollLayout.addWidget(postOptionsLayout)
    def spawnImages(*kwargs):
        utils.consolelog('utils.spawnImages({})'.format(kwargs))
        for image in kwargs:
            if (image not in ['.']):
                fn = utils.getImageDataUsingUrl(image)
                utils.mkimage(fn)
    def queryImages(amount, subreddit, clearPrevious = False):
        utils.consolelog('utils.queryImages({}, {}, clearPrevious = {})'.format(amount, subreddit, clearPrevious))
        global ut, previousImages, previousLoadAmounts
        if (clearPrevious):
            utils.clearMCD()
        urllist = reddit_bot.subreddit(subreddit).new(limit = amount)
        for url in urllist:
            ut = url.title
            if (url.url not in previousImages):
                utils.spawnImages(url.url)
            previousImages.append(str(url.url))
            if (subreddit not in previousLoadAmounts):
                previousLoadAmounts[subreddit] = 1
            else:
                previousLoadAmounts[subreddit] += 1
        window.setWindowTitle('PC Reddit browser - r/{}'.format(subreddit))
    def saveFile(filename):
        utils.consolelog('utils.savefile({})'.format(filename))
        shutil.copyfile(('./tmp/' + filename), ('C:\\Users\\{}\\Pictures\\{}'.format(os.getlogin(), filename)))
    def clearMCD():
        utils.consolelog('utils.clearMCD()')
        global scrollLayout
        for i in reversed(range(scrollLayout.count())): 
            scrollLayout.itemAt(i).widget().deleteLater()
    def loadMore(amount):
        utils.consolelog('utils.loadmore({})'.format(amount))
        global previousImages, previousLoadAmounts, subreddit_current
        subreddit_current = sidebarScroll_e1.toPlainText()
        try:
            if (subreddit_current not in previousLoadAmounts):
                utils.queryImages(amount, subreddit_current)
            else:
                utils.queryImages((previousLoadAmounts[subreddit_current]), subreddit_current)
        except:
            print ('Error retriving photos. (Did I spell that right?)')

window.resize(500, 500)
window.show()

def windowResizeThread():
    global application_running, actualMCA
    while (application_running):
        scroll.resize(actualMCA, window.height())
        sidebarScroll.resize(sidebarMinWidth, window.height())
        sidebarScroll.move(actualMCA, 0)
        console.resize((window.width() - (actualMCA + sidebarMinWidth)), window.height())

utils.consolelog('Starting console...')
resizeThread = thread.start_new_thread(windowResizeThread, ())
utils.queryImages(1, 'aviation')
application.exec_()

application_running = False

for item in os.listdir('./tmp'):
    os.remove('./tmp/{}'.format(item))