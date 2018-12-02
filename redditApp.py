#requires [praw, PyQt5, _thread, sys, urllib, os]

import praw as praw
import PyQt5 as PyQt5
from PyQt5.QtWidgets import *
import _thread as thread
import sys as sys
import urllib as urllib
import os as os

if ('tmp' not in os.listdir('.')):
    os.mkdir('tmp')

reddit_bot = praw.Reddit(user_agent = 'katznbot', client_id = '_CIuAjxI8TaKvg', client_secret = 'HnpYVUD2jouM--6OdFzdFNJ_g2E', username = 'katznbot', password = '')
reddit_subreddit = 'cats'
reddit_sortby = 'new'

application_running = True
application_ytop = 0

application = QApplication(sys.argv)

ut = ''

mainContentAreaWidth = 500

window = QWidget()
window.setWindowTitle('PC reddit browser')
window.setMinimumSize(400, 400)
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

class utils():
    def getImageDataUsingUrl(url):
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
        vor.setText('{}\n(Title of image above)'.format(ut))
        scrollLayout.addWidget(vor)
        postOptionsLayout = QWidget()
        l1 = QHBoxLayout()
        l1_b1 = QPushButton()
        l1_b1.setText('Save')
        l1_b1.setStyleSheet('QPushButton{background-color:lightgray;color:black;border:1px solid black;font-family:Verdana;font-size:13px;}')
        l1.addWidget(l1_b1)
        l1_b2 = QPushButton()
        l1_b2.setText('View on reddit.com')
        l1_b2.setStyleSheet('QPushButton{background-color:lightgray;color:black;border:1px solid black;font-family:Verdana;font-size:13px;}')
        l1.addWidget(l1_b2)
        l1_b3 = QPushButton()
        l1_b3.setText('Share')
        l1_b3.setStyleSheet('QPushButton{background-color:lightgray;color:black;border:1px solid black;font-family:Verdana;font-size:13px;}')
        l1.addWidget(l1_b3)
        postOptionsLayout.setLayout(l1)
        scrollLayout.addWidget(postOptionsLayout)
    def spawnImages(*kwargs):
        for image in kwargs:
            if (image not in ['.']):
                fn = utils.getImageDataUsingUrl(image)
                utils.mkimage(fn)
    def queryImages(amount, subreddit):
        urllist = reddit_bot.subreddit(subreddit).new(limit = amount)
        for url in urllist:
            ut = url.title
            utils.spawnImages(url.url)

window.resize(500, 500)
window.show()

def windowResizeThread():
    global application_running, mainContentAreaWidth
    while (application_running):
        scroll.resize(mainContentAreaWidth, window.height())
        sidebarScroll.resize((window.width() - mainContentAreaWidth), window.height())
        sidebarScroll.move(mainContentAreaWidth, 0)

resizeThread = thread.start_new_thread(windowResizeThread, ())
utils.queryImages(20, 'cats')
application.exec_()

application_running = False

for item in os.listdir('./tmp'):
    os.remove('./tmp/{}'.format(item))