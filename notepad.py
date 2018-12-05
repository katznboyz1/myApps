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

filename = ''

header_bar = QMenuBar(window)
header_bar.resize(window.width(), 20)
header_bar.move(0, 0)

header_filebutton1 = header_bar.addMenu('File')
header_filebutton1.setGeometry(0, 0, 40, 20)
header_filebutton1.updateGeometry()
header_filebutton1.addAction('New').triggered.connect(lambda: buttonPressRegister('clearTextArea'))
header_filebutton1.addAction('Open...').triggered.connect(lambda: buttonPressRegister('openNew'))
header_filebutton1.addAction('Save').triggered.connect(lambda: buttonPressRegister('saveFile'))
header_filebutton1.addAction('Save as...').triggered.connect(lambda: buttonPressRegister('saveFileAs'))
header_filebutton1.setStyleSheet(headermenuss)

header_filebutton2 = header_bar.addMenu('Edit')
header_filebutton2.setGeometry((header_filebutton1.width() + header_filebutton1.x()), 0, 40, 20)
header_filebutton2.updateGeometry()
header_filebutton2.addAction('Undo').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton2.addAction('Cut').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton2.addAction('Copy').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton2.addAction('Paste').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton2.addAction('Delete').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton2.addAction('Find...').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton2.addAction('Find Next').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton2.addAction('Replace...').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton2.addAction('Go To...').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton2.setStyleSheet(headermenuss)

header_filebutton3 = header_bar.addMenu('Format')
header_filebutton3.setGeometry((header_filebutton2.width() + header_filebutton2.x()), 0, 60, 20)
header_filebutton3.updateGeometry()
header_filebutton3.addAction('Word Wrap').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton3.addAction('Font...').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton3.setStyleSheet(headermenuss)

header_filebutton4 = header_bar.addMenu('View')
header_filebutton4.setGeometry((header_filebutton3.width() + header_filebutton3.x()), 0, 60, 20)
header_filebutton4.updateGeometry()
header_filebutton4.addAction('Status Bar').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton4.setStyleSheet(headermenuss)

header_filebutton5 = header_bar.addMenu('Help')
header_filebutton5.setGeometry((header_filebutton4.width() + header_filebutton4.x()), 0, 60, 20)
header_filebutton5.updateGeometry()
header_filebutton5.addAction('View Help').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton5.addAction('About Notepad').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton5.setStyleSheet(headermenuss)

textEntry = QPlainTextEdit(window)
textEntry.move(0, header_filebutton1.height())
textEntry.resize(window.width(), (window.height() - header_filebutton1.height()))
textEntry.setStyleSheet('QPlainTextEdit{background-color:white;border-top:2px solid #c2c2c2;font-family:Consolas;font-size:15px;}')

def buttonPressRegister(command):
    global filename
    commmand = str(command)
    if (command == 'clearTextArea'):
        textEntry.setPlainText('')
    elif (command == 'openNew'):
        _filename = QFileDialog.getOpenFileName()[0]
        file = open(_filename, 'r')
        textEntry.setPlainText(str(file.read()))
        file.close()
        window.setWindowTitle(_filename)
    elif (command == 'saveFile'):
        if (filename == ''):
            buttonPressRegister('saveFileAs')
        else:
            file = open(filename, 'w')
            file.write(str(textEntry.toPlainText()))
            file.close()
    elif (command == 'saveFileAs'):
        _filename = QFileDialog.getOpenFileName()[0]
        filename = _filename
        buttonPressRegister('saveFile')
        window.setWindowTitle(filename)

def resizeThread():
    global applicationRunning
    while (applicationRunning):
        textEntry.resize(window.width(), (window.height() - 20))
        header_bar.resize(window.width(), 20)

thread.start_new_thread(resizeThread, ())

window.show()
application.exec_()

applicationRunning = False
