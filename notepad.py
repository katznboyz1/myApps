import PyQt5 as PyQt5
from PyQt5.QtWidgets import *
import sys as sys
import _thread as thread

applicationRunning = True

application = QApplication(sys.argv)

screen = application.primaryScreen()

window = QWidget()
window.setWindowTitle('Untitled - Notepad')
window.setStyleSheet('QWidget{background-color:white;}')
window.setMinimumSize(400, 200)
window.resize((screen.size().width() / 2), (screen.size().height() / 2))

headermenuss = '''
QPushButton{font-family:Calibri;font-size:14px;background-color:white;color:black;text-align:center;border:0px;}
QPushButton:hover{font-family:Calibri;font-size:14px;background-color:#ccf7ff;color:black;text-align:center;border:1px solid #83a3a8;}
'''

#figure out how to make it so that when one of the options is clicked an event happens

header_bar = QMenuBar(window)
header_bar.resize(window.width(), 20)
header_bar.move(0, 0)

header_filebutton1 = header_bar.addMenu('File')
header_filebutton1.setGeometry(0, 0, 40, 20)
header_filebutton1.updateGeometry()
header_filebutton1.addAction('New')
header_filebutton1.addAction('Open...')
header_filebutton1.addAction('Save')
header_filebutton1.addAction('Save as...')
header_filebutton1.setStyleSheet(headermenuss)

header_filebutton2 = header_bar.addMenu('Edit')
header_filebutton2.setGeometry((header_filebutton1.width() + header_filebutton1.x()), 0, 40, 20)
header_filebutton2.updateGeometry()
header_filebutton2.addAction('Undo')
header_filebutton2.addAction('Cut')
header_filebutton2.addAction('Copy')
header_filebutton2.addAction('Paste')
header_filebutton2.addAction('Delete')
header_filebutton2.addAction('Find...')
header_filebutton2.addAction('Find Next')
header_filebutton2.addAction('Replace...')
header_filebutton2.addAction('Go To...')
header_filebutton2.setStyleSheet(headermenuss)

header_filebutton3 = header_bar.addMenu('Format')
header_filebutton3.setGeometry((header_filebutton2.width() + header_filebutton2.x()), 0, 60, 20)
header_filebutton3.updateGeometry()
header_filebutton3.addAction('Word Wrap')
header_filebutton3.addAction('Font...')
header_filebutton3.setStyleSheet(headermenuss)

header_filebutton4 = header_bar.addMenu('View')
header_filebutton4.setGeometry((header_filebutton3.width() + header_filebutton3.x()), 0, 60, 20)
header_filebutton4.updateGeometry()
header_filebutton4.addAction('Status Bar')
header_filebutton4.setStyleSheet(headermenuss)

header_filebutton5 = header_bar.addMenu('Help')
header_filebutton5.setGeometry((header_filebutton4.width() + header_filebutton4.x()), 0, 60, 20)
header_filebutton5.updateGeometry()
header_filebutton5.addAction('View Help')
header_filebutton5.addAction('About Notepad')
header_filebutton5.setStyleSheet(headermenuss)

textEntry = QPlainTextEdit(window)
textEntry.move(0, header_filebutton1.height())
textEntry.resize(window.width(), (window.height() - header_filebutton1.height()))
textEntry.setStyleSheet('QPlainTextEdit{background-color:white;border-top:2px solid #c2c2c2;font-family:Consolas;font-size:15px;}')

def resizeThread():
    global applicationRunning
    while (applicationRunning):
        textEntry.resize(window.width(), (window.height() - header_filebutton1.height()))
        header_bar.resize(window.width(), 20)

thread.start_new_thread(resizeThread, ())

window.show()
application.exec_()

applicationRunning = False
