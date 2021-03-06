import PyQt5 as PyQt5
from PyQt5.QtWidgets import *
import sys as sys
import _thread as thread
import os as os

def buttonPressRegister(command):
    global filename
    commmand = str(command)
    if (command == 'clearTextArea'):
        textEntry.setPlainText('')
        filename = ''
        window.setWindowTitle('Untitled - Notepad')
    elif (command == 'openNew'):
        try:
            _filename = QFileDialog.getOpenFileName()[0]
            file = open(_filename, 'r')
            textEntry.setPlainText(str(file.read()))
            file.close()
            window.setWindowTitle(_filename)
            filename = _filename
        except FileNotFoundError as err:
            buttonPressRegister('error:File was not found. (FileNotFoundError)')
        except UnicodeDecodeError as err:
            buttonPressRegister('error:Notepad cant open images. (UnicodeDecodeError)')
    elif (command == 'saveFile'):
        if (filename == ''):
            buttonPressRegister('saveFileAs')
        else:
            try:
                file = open(filename, 'w')
                file.write(str(textEntry.toPlainText()))
                file.close()
            except FileNotFoundError as err:
                buttonPressRegister('error:File was not found. (FileNotFoundError)')
    elif (command == 'saveFileAs'):
        _filename = QFileDialog.getSaveFileName()[0]
        filename = _filename
        if (filename == ''):
            pass
        else:
            buttonPressRegister('saveFile')
            window.setWindowTitle(filename)
    elif (command.split(':')[0] == 'error'):
        errorDialog = QErrorMessage(window)
        if (command.count(':') == 1):
            err = command.split(':')[1]
        else:
            err = 'Error.'
        errorDialog.showMessage(err)
        errorDialog.setWindowTitle('Notepad - Error')
    elif (command == 'viewHelp'):
        try:
            os.startfile('help.html')
        except FileNotFoundError as err:
            buttonPressRegister('error:Help file not found. (FileNotFoundError)')
    elif (command == ''):
        print ('This command is a work in progress.')
    else:
        buttonPressRegister('error:Unknown argument for __main__.buttonPressRegister. Please notify the author about this. Command was("{}")'.format(command))

applicationRunning = True

application = QApplication(sys.argv)

screen = application.primaryScreen()

window = QWidget()
window.setWindowTitle('Untitled - Notepad')
window.setStyleSheet('QWidget{background-color:white;}')
window.setMinimumSize(400, 200)
window.resize((screen.size().width() / 2), (screen.size().height() / 2))
try:
    window.setWindowIcon(PyQt5.QtGui.QIcon('icon.png'))
except:
    buttonPressRegister('error:Application icon not found. (./icon.png)')

headermenuss = '''
QPushButton{font-family:Calibri;font-size:14px;background-color:white;color:black;text-align:center;border:0px;}
QPushButton:hover{font-family:Calibri;font-size:14px;background-color:#ccf7ff;color:black;text-align:center;border:1px solid #83a3a8;}
'''

qass = '''
QMenu{background-color:#ededed;border:1px solid #636361;color:black}
''' #this isnt working for the background color or border

filename = ''

header_bar = QMenuBar(window)
header_bar.resize(window.width(), 20)
header_bar.move(0, 0)

header_filebutton1 = header_bar.addMenu('File')
header_filebutton1.setStyleSheet(qass)
header_filebutton1.setGeometry(0, 0, 40, 20)
shortcutrequire1 = header_filebutton1.addAction('New')
shortcutrequire1.triggered.connect(lambda: buttonPressRegister('clearTextArea'))
shortcutrequire1.setShortcut('Ctrl+N')
shortcutrequire2 = header_filebutton1.addAction('Open...')
shortcutrequire2.triggered.connect(lambda: buttonPressRegister('openNew'))
shortcutrequire2.setShortcut('Ctrl+O')
shortcutrequire3 = header_filebutton1.addAction('Save')
shortcutrequire3.triggered.connect(lambda: buttonPressRegister('saveFile'))
shortcutrequire3.setShortcut('Ctrl+S')
header_filebutton1.addAction('Save as...').triggered.connect(lambda: buttonPressRegister('saveFileAs'))
header_filebutton1.addAction('Page Setup').triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire4 = header_filebutton1.addAction('Print')
shortcutrequire4.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire4.setShortcut('Ctrl+P')
header_filebutton1.addAction('Exit').triggered.connect(lambda: exit())
header_filebutton1.setStyleSheet(headermenuss)

header_filebutton2 = header_bar.addMenu('Edit')
header_filebutton2.setStyleSheet(qass)
header_filebutton2.setGeometry((header_filebutton1.width() + header_filebutton1.x()), 0, 40, 20)
header_filebutton2.updateGeometry()
shortcutrequire5 = header_filebutton2.addAction('Undo')
shortcutrequire5.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire5.setShortcut('Ctrl+Z')
shortcutrequire6 = header_filebutton2.addAction('Cut')
shortcutrequire6.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire6.setShortcut('Ctrl+X')
shortcutrequire7 = header_filebutton2.addAction('Copy')
shortcutrequire7.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire7.setShortcut('Ctrl+C')
shortcutrequire8 = header_filebutton2.addAction('Paste')
shortcutrequire8.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire8.setShortcut('Ctrl+V')
shortcutrequire9 = header_filebutton2.addAction('Delete')
shortcutrequire9.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire9.setShortcut('Del')
shortcutrequire10 = header_filebutton2.addAction('Find...')
shortcutrequire10.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire10.setShortcut('Ctrl+F')
shortcutrequire11 = header_filebutton2.addAction('Find Next')
shortcutrequire11.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire11.setShortcut('F3')
shortcutrequire12 = header_filebutton2.addAction('Replace...')
shortcutrequire12.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire12.setShortcut('Ctrl+H')
shortcutrequire13 = header_filebutton2.addAction('Go To...')
shortcutrequire13.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire13.setShortcut('Ctrl+G')
shortcutrequire14 = header_filebutton2.addAction('Select All')
shortcutrequire14.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire14.setShortcut('Ctrl+A')
shortcutrequire15 = header_filebutton2.addAction('Time/Date')
shortcutrequire15.triggered.connect(lambda: buttonPressRegister(''))
shortcutrequire15.setShortcut('F5')
header_filebutton2.setStyleSheet(headermenuss)

header_filebutton3 = header_bar.addMenu('Format')
header_filebutton3.setStyleSheet(qass)
header_filebutton3.setGeometry((header_filebutton2.width() + header_filebutton2.x()), 0, 60, 20)
header_filebutton3.updateGeometry()
header_filebutton3.addAction('Word Wrap').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton3.addAction('Font...').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton3.setStyleSheet(headermenuss)

header_filebutton4 = header_bar.addMenu('View')
header_filebutton4.setStyleSheet(qass)
header_filebutton4.setGeometry((header_filebutton3.width() + header_filebutton3.x()), 0, 60, 20)
header_filebutton4.updateGeometry()
header_filebutton4.addAction('Status Bar').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton4.setStyleSheet(headermenuss)

header_filebutton5 = header_bar.addMenu('Help')
header_filebutton5.setStyleSheet(qass)
header_filebutton5.setGeometry((header_filebutton4.width() + header_filebutton4.x()), 0, 60, 20)
header_filebutton5.updateGeometry()
header_filebutton5.addAction('View Help').triggered.connect(lambda: buttonPressRegister('viewHelp'))
header_filebutton5.addAction('About Notepad').triggered.connect(lambda: buttonPressRegister(''))
header_filebutton5.setStyleSheet(headermenuss)

textEntry = QPlainTextEdit(window)
textEntry.move(0, header_filebutton1.height())
textEntry.resize(window.width(), (window.height() - header_filebutton1.height()))
textEntry.setStyleSheet('QPlainTextEdit{background-color:white;border-top:2px solid #c2c2c2;font-family:Consolas;font-size:15px;}')

def resizeThread():
    global applicationRunning
    while (applicationRunning):
        textEntry.resize(window.width(), (window.height() - 20))
        header_bar.resize(window.width(), 20)

thread.start_new_thread(resizeThread, ())

window.show()
application.exec_()

applicationRunning = False
