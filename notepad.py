#Buttons dont work yet

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

headerbuttonss = '''
QPushButton{font-family:Calibri;font-size:14px;background-color:white;color:black;text-align:center;border:0px;}
QPushButton:hover{font-family:Calibri;font-size:14px;background-color:#ccf7ff;color:black;text-align:center;border:1px solid #83a3a8;}
'''

header_filebutton1 = QPushButton(window)
header_filebutton1.setStyleSheet(headerbuttonss)
header_filebutton1.setText('File')
header_filebutton1.resize(40, 20)
header_filebutton1.move(0, 0)

header_filebutton2 = QPushButton(window)
header_filebutton2.setStyleSheet(headerbuttonss)
header_filebutton2.setText('Edit')
header_filebutton2.resize(40, 20)
header_filebutton2.move((header_filebutton1.x() + header_filebutton1.width()), 0)

header_filebutton3 = QPushButton(window)
header_filebutton3.setStyleSheet(headerbuttonss)
header_filebutton3.setText('Format')
header_filebutton3.resize(60, 20)
header_filebutton3.move((header_filebutton2.x() + header_filebutton2.width()), 0)

header_filebutton4 = QPushButton(window)
header_filebutton4.setStyleSheet(headerbuttonss)
header_filebutton4.setText('View')
header_filebutton4.resize(40, 20)
header_filebutton4.move((header_filebutton3.x() + header_filebutton3.width()), 0)

header_filebutton5 = QPushButton(window)
header_filebutton5.setStyleSheet(headerbuttonss)
header_filebutton5.setText('Help')
header_filebutton5.resize(40, 20)
header_filebutton5.move((header_filebutton4.x() + header_filebutton4.width()), 0)

textEntry = QPlainTextEdit(window)
textEntry.move(0, header_filebutton1.height())
textEntry.resize(window.width(), (window.height() - header_filebutton1.height()))
textEntry.setStyleSheet('QPlainTextEdit{background-color:white;border-top:2px solid #c2c2c2;font-family:Consolas;font-size:15px;}')

def resizeThread():
    global applicationRunning
    while (applicationRunning):
        textEntry.resize(window.width(), (window.height() - header_filebutton1.height()))

thread.start_new_thread(resizeThread, ())

window.show()
application.exec_()

applicationRunning = False