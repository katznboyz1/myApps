import PyQt5 as PyQt5
from PyQt5.QtWidgets import *
import sys as sys
import _thread as thread
import os as os
import urllib as urllib
import praw as praw
import shutil as shutil

application = QApplication(sys.argv)

screen = application.primaryScreen()

class reddit():
    reddit_bot = praw.Reddit(user_agent = 'katznbot', client_id = '_CIuAjxI8TaKvg', client_secret = 'HnpYVUD2jouM--6OdFzdFNJ_g2E', username = 'katznbot', password = '') #this can be public, its just a reddit bot.
    subreddit = 'all'

class app():
    applicationRunning = True
    loadedImageURLs = []
    previousLoadCounts = {}
    windowState = 'min'
    defaultTitle = 'Reddit App V2'
    mainContentAreaWidth = 700
    loadAmount = 5

if ('tmp' not in os.listdir('.')):
    os.mkdir('tmp')

for file in os.listdir('./tmp'):
    os.remove('./tmp/' + file)

def event(e):
    e = str(e)
    if (e == 'exit'):
        app.applicationRunning = False
        exit()
    elif (e == 'minimizeWindow'):
        window.showMinimized()
    elif (e == 'toggleWindowSizeState'):
        if (app.windowState == 'min'):
            window.showMaximized()
            app.windowState = 'max'
        else:
            window.showNormal()
            app.windowState = 'min'
    elif (e.split('\u2588')[0] == 'setWindowTitle'):
        windowTitle.setText(e.split('\u2588')[1])
    elif (e.split('\u2588')[0] == 'error'):
        err = e.split('\u2588')[1]
        errorDialog = QErrorMessage(errWidget)
        errorDialog.showMessage(err)
        errorDialog.setWindowTitle('{} - Error'.format(app.defaultTitle))
        errorDialog.setStyleSheet('QErrorMessage{color:white;}')

class headerMonitoring():
    offset = None
    def windowDrag(e):
        headerMonitoring.offset = e.pos()
    def windowMove(e):
        x = e.globalX()
        y = e.globalY()
        x_w = headerMonitoring.offset.x()
        y_w = headerMonitoring.offset.y()
        window.move((x - x_w), (y - y_w))

def getImage(url):
    url = str(url)
    imagefilename = str(url).split('/')[(url.count('/'))]
    imagefilename = imagefilename.split(':')[(imagefilename.count(':'))]
    fp = './tmp/' + imagefilename
    imageContents = urllib.request.urlopen(url)
    image = open(('./tmp/' + imagefilename), 'wb')
    image.write(imageContents.read())
    image.close()
    app.loadedImageURLs.append(url)
    return fp

def retriveImagesFromSubreddit(subreddit, limit = 5):
    if (subreddit not in app.previousLoadCounts):
        app.previousLoadCounts[subreddit] = limit
    else:
        limit += app.previousLoadCounts[subreddit]
    retrivedUrls = reddit.reddit_bot.subreddit(subreddit).new(limit = limit)
    return retrivedUrls

def addImageToScreen(filepath, title = 'Error loading post.', nativeUrl = 'about:blank'):
    global scrollLayout
    pic = QLabel()
    pic.resize(300, 300)
    pixmap = PyQt5.QtGui.QPixmap(filepath)
    try:
        img_aspect_ratio = (float(pixmap.size().width()) / pixmap.size().height())
    except:
        img_aspect_ratio = 1.8
    width = app.mainContentAreaWidth - 20
    height = (app.mainContentAreaWidth / img_aspect_ratio)
    pixmap = pixmap.scaled(width, height)
    pic.setPixmap(pixmap)
    pic.resize(width, height)
    pic.setStyleSheet('QLabel{background-color:transparent;}')
    scrollLayout.addWidget(pic)
    imgTitle = QLabel()
    imgTitle.setWordWrap(True)
    imgTitle.setText(title)
    imgTitle.setStyleSheet('QLabel{background-color:transparent;color:white;font-size:14px;}')
    scrollLayout.addWidget(imgTitle)
    postOptionsLayout = QWidget()
    lbss = '''
QPushButton{background-color:lightgray;color:black;border:1px solid black;font-family:Verdana;font-size:13px;margin:0px;}
QPushButton:hover{background-color:white;color:black;border:1px solid black;font-family:Verdana;font-size:13px;margin:0px;}
'''
    l1 = QHBoxLayout()
    l1_b1 = QPushButton()
    l1_b1.setText('Save')
    l1_b1.setStyleSheet(lbss)
    l1_b1.setFixedSize((app.mainContentAreaWidth / 3.5), 25)
    l1_b1.clicked.connect(lambda: saveFile(filepath))
    l1.addWidget(l1_b1)
    l1_b2 = QPushButton()
    l1_b2.setText('View in browser')
    l1_b2.setStyleSheet(lbss)
    l1_b2.setFixedSize((app.mainContentAreaWidth / 3.5), 25)
    l1_b2.clicked.connect(lambda: os.startfile(nativeUrl))
    l1.addWidget(l1_b2)
    l1_b3 = QPushButton()
    l1_b3.setText('Share')
    l1_b3.setStyleSheet(lbss)
    l1_b3.setFixedSize((app.mainContentAreaWidth / 3.5), 25)
    l1_b3.clicked.connect(lambda: event(('error\u2588This button does not work in the current version of this app.')))
    l1.addWidget(l1_b3)
    postOptionsLayout.setLayout(l1)
    scrollLayout.addWidget(postOptionsLayout)
    window.update() #doesnt update window ;-;

def saveFile(filename):
    shutil.copyfile((filename), ('C:\\Users\\{}\\Pictures\\{}'.format(os.getlogin(), filename.split('/')[filename.count('/')])))

def loadFromSubreddit(subreddit, limit):
    sla(loadAmntEntry.toPlainText())
    event('setWindowTitle\u2588{} - Loading...'.format(app.defaultTitle))
    images = retriveImagesFromSubreddit(subreddit, limit = limit)
    for url in images:
        try:
            if (url.url not in app.loadedImageURLs):
                img = getImage(url.url)
            addImageToScreen(img, title = url.title, nativeUrl = url.url)
        except Exception as err:
            pass
    event('setWindowTitle\u2588{} - r/{}'.format(app.defaultTitle, subreddit))

def sla(amount):
    try:
        amount = int(amount)
        app.loadAmount = amount
    except Exception as err:
        event('error\u2588{}'.format(err))

window = QWidget()
window.setWindowTitle('Reddit App V2')
window.setStyleSheet('QWidget{background-color:#2b2b2b;}')
window.setWindowIcon(PyQt5.QtGui.QIcon('reddit_application_icon.png'))
window.resize((screen.size().width() / 2), (screen.size().height() / 2))
window.setWindowFlags(PyQt5.QtCore.Qt.CustomizeWindowHint) 

errWidget = QWidget(window)
errWidget.resize(0, 0)
errWidget.setStyleSheet('QWidget{background-color:white;}')

windowTopBorder = QWidget(window)
windowTopBorder.resize(window.width(), 20)
windowTopBorder.move(0, 0)
windowTopBorder.setStyleSheet('QWidget{background-color:black;}')
windowTopBorder.mousePressEvent = lambda e: headerMonitoring.windowDrag(e)
windowTopBorder.mouseMoveEvent = lambda e: headerMonitoring.windowMove(e)

windowTitle = QLabel(window)
windowTitle.move(10, 0)
windowTitle.setFixedHeight(20)
windowTitle.setStyleSheet('QLabel{color:white;font-family:Calibri;background-color:transparent;qproperty-alignment:AlignCenter;}')
windowTitle.mousePressEvent = lambda e: headerMonitoring.windowDrag(e)
windowTitle.mouseMoveEvent = lambda e: headerMonitoring.windowMove(e)
windowTitle.setFixedWidth(window.width())

exitButton = QPushButton(window)
exitButton.move((window.width() - exitButton.width()), 0)
exitButton.setText('X')
exitButton.resize(40, 20)
exitButton.setStyleSheet('''
QPushButton{background-color:transparent;color:white;font-family:Courier;}
QPushButton:hover{background-color:red;color:white;font-family:Courier;}
''')
exitButton.clicked.connect(lambda: event('exit'))

toggleWindowStateButton = QPushButton(window)
toggleWindowStateButton.move((exitButton.x() - exitButton.width()), 0)
toggleWindowStateButton.setText('[]')
toggleWindowStateButton.resize(40, 20)
toggleWindowStateButton.setStyleSheet('''
QPushButton{background-color:transparent;color:white;font-family:Courier;}
QPushButton:hover{background-color:#6b6a6a;color:white;font-family:Courier;}
''')
toggleWindowStateButton.clicked.connect(lambda: event('toggleWindowSizeState'))

minimizeButton = QPushButton(window)
minimizeButton.move((toggleWindowStateButton.x() - toggleWindowStateButton.width()), 0)
minimizeButton.setText('-')
minimizeButton.resize(40, 20)
minimizeButton.setStyleSheet('''
QPushButton{background-color:transparent;color:white;font-family:Courier;}
QPushButton:hover{background-color:#6b6a6a;color:white;font-family:Courier;}
''')
minimizeButton.clicked.connect(lambda: event('minimizeWindow'))

scroll = QScrollArea(window)
scroll.setWidgetResizable(True)
scrollContent = QWidget(scroll)
scrollLayout = QVBoxLayout(scrollContent)
scrollContent.setLayout(scrollLayout)
scroll.setWidget(scrollContent)
scroll.resize(app.mainContentAreaWidth, 500)
scroll.move(0, windowTopBorder.height())
scroll.setStyleSheet('QScrollArea{border:none;border-right:2px solid black;}')

sidebarDiv = QWidget(window)
sidebarDiv.resize((window.width() - app.mainContentAreaWidth), window.height())
sidebarDiv.setStyleSheet('QWidget{background-color:transparent;}')
sidebarDiv.move(app.mainContentAreaWidth, windowTopBorder.height())

sidebarDivButtonSS = '''
QToolButton{background-color:#a8a8a8;color:black;font-size:15px;border:2px solid black;}
QToolButton:hover{background-color:white;color:black;font-size:15px;border:2px solid #00665f;}
QPlainTextEdit{background-color:#a8a8a8;color:black;font-size:14px;border:2px solid black;}
QPlainTextEdit:hover{background-color:white;color:black;font-size:14px;border:2px solid #00665f;}
'''

loadMoreButton = QToolButton(sidebarDiv)
loadMoreButton.setText('Click here to load\nmore images from:')
loadMoreButton.setStyleSheet(sidebarDivButtonSS)
loadMoreButton.move(0, 0)
loadMoreButton.resize(170, 50)
loadMoreButton.clicked.connect(lambda: loadFromSubreddit(loadMoreEntry.toPlainText(), app.loadAmount))

loadMoreEntry = QPlainTextEdit(sidebarDiv)
loadMoreEntry.resize(loadMoreButton.width(), loadMoreButton.height())
loadMoreEntry.move(loadMoreButton.width(), 0)
loadMoreEntry.setStyleSheet(sidebarDivButtonSS)
loadMoreEntry.setPlainText('aviation')

loadAmntButton = QToolButton(sidebarDiv)
loadAmntButton.setText('Click here to set\nimage load amount:')
loadAmntButton.setStyleSheet(sidebarDivButtonSS)
loadAmntButton.move(0, (loadMoreButton.height()))
loadAmntButton.resize(170, 50)
loadAmntButton.clicked.connect(lambda: sla(loadAmntEntry.toPlainText()))

loadAmntEntry = QPlainTextEdit(sidebarDiv)
loadAmntEntry.resize(loadMoreButton.width(), loadMoreButton.height())
loadAmntEntry.move(loadMoreButton.width(), (loadAmntButton.y()))
loadAmntEntry.setStyleSheet(sidebarDivButtonSS)
loadAmntEntry.setPlainText(str(app.loadAmount))

def resizeThread():
    while (app.applicationRunning):
        exitButton.move((window.width() - exitButton.width()), 0)
        toggleWindowStateButton.move((exitButton.x() - exitButton.width()), 0)
        minimizeButton.move((toggleWindowStateButton.x() - toggleWindowStateButton.width()), 0)
        windowTopBorder.resize(window.width(), 20)
        scroll.resize(app.mainContentAreaWidth, (window.height() - windowTopBorder.height()))
        windowTitle.setFixedWidth(window.width())
        sidebarDiv.resize((window.width() - app.mainContentAreaWidth), window.height())

event('setWindowTitle\u2588{}'.format(app.defaultTitle))

window.setMinimumSize(scroll.width(), 300)

thread.start_new_thread(resizeThread, ())

window.show()
window.resize((app.mainContentAreaWidth + loadAmntButton.width() + loadAmntEntry.width()), 500)

application.exec_()

applicationRunning = False

for file in os.listdir('./tmp'):
    os.remove('./tmp/' + file)
