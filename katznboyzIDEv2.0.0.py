import PyQt5, sys, _thread, os
from PyQt5.QtWidgets import *

buttonStyleSheetNo1 = '''
QPushButton{background-color:#292929;color:white;font-size:15px;border:2px solid #292929;border-radius:5px;font-family:Verdana;}
QPushButton:hover{background-color:#403f3e;color:white;font-size:15px;border:2px solid #292929;border-radius:5px;font-family:Verdana;}
QPlainTextEdit{background-color:#292929;color:white;font-size:15px;border:2px solid #292929;border-radius:5px;font-family:Verdana;}
QPlainTextEdit:hover{background-color:#403f3e;color:white;font-size:15px;border:2px solid #292929;border-radius:5px;font-family:Verdana;}
'''

application = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Katznboyz IDE -- Version 2.0.0 (BETA)')

mainTextArea = QPlainTextEdit(window)
mainTextArea.setStyleSheet('QPlainTextEdit{background-color:#363636;font-size:15px;font-family:Consolas;color:white;border:none;}')
mainTextArea.move(300, 0)

openButton = QPushButton(window)
openButton.setStyleSheet(buttonStyleSheetNo1)
openButton.setText('Open file:')
openButton.move(0, 0)
openButton.clicked.connect(lambda: openSelectedFile())
openButton.resize(175, 25)

openTextArea = QPlainTextEdit(window)
openTextArea.setStyleSheet(buttonStyleSheetNo1)
openTextArea.move(openButton.width(), 0)
openTextArea.resize(125, openButton.height())

saveButton = QPushButton(window)
saveButton.setStyleSheet(buttonStyleSheetNo1)
saveButton.setText('Save to/make\nfile:')
saveButton.move(0, (openButton.y() + openButton.height() + 3))
saveButton.clicked.connect(lambda: saveSelectedFile())
saveButton.resize(175, 50)

saveTextArea = QPlainTextEdit(window)
saveTextArea.setStyleSheet(buttonStyleSheetNo1)
saveTextArea.move(saveButton.width(), saveButton.y())
saveTextArea.resize(125, saveButton.height())

scroll = QScrollArea(window)
scroll.setWidgetResizable(True)
scrollContent = QWidget(scroll)
scrollLayout = QVBoxLayout(scrollContent)
scrollContent.setLayout(scrollLayout)
scroll.setWidget(scrollContent)
scroll.move(0, saveTextArea.y() + 100)
scroll.resize(300, (window.height() - scroll.y()))

def makeFB1(topy, currentscandirindex, files):
    global scrollLayout
    attrb = QPushButton()
    attrb.setText(files)
    attrb.setStyleSheet('''QPushButton{background-color:#1c1c1c;color:white;border:1px solid black;font-size:15px;}\nQPushButton:hover{background-color:black;color:white;border:1px solid black;font-size:15px;}''')
    attrb.setFixedWidth(260)
    attrb.setFixedHeight(60)
    attrb.clicked.connect(lambda: openSelectedFile(filename = files))
    scrollLayout.addWidget(attrb)

try:
    currentscandirindex = 0
    topy = (saveButton.y() + saveButton.height())
    for files in os.listdir('.'): #trying to open a folder will result in permissionerror (FIX THIS NOW!)
        currentscandirindex += 1  #make this inside a scrollable div
        makeFB1(topy, currentscandirindex, files)
except:
    print ('permissionerror while scanning dir')

def openSelectedFile(filename = ''):
    global openTextArea, mainTextArea, window
    if filename == '':
        filename = openTextArea.toPlainText()
    try:
        fileo = open(filename, 'r')
        filecontents = fileo.read()
        fileo.close()
        mainTextArea.setPlainText(filecontents)
        window.setWindowTitle('KatznboyzIDE - {}'.format(filename))
        saveTextArea.setPlainText(filename)

    except:
        print ('Error opening file')

def saveSelectedFile():
    global saveTextArea, mainTextArea
    filename = saveTextArea.toPlainText()
    filecontents = mainTextArea.toPlainText()
    try:
        fileo = open(filename, 'w')
        fileo.write(filecontents)
        fileo.close()
    except:
        print ('Error saving to file')

def main():
    global mainTextArea, openButton, openTextArea
    mainTextArea.move(300, 0)
    mainTextArea.setFixedWidth((window.width() - 200))
    mainTextArea.setFixedHeight(window.height())
    scroll.resize(300, (window.height() - scroll.y()))

thread_variable_lastscreensize = [window.width(), window.height()]
def thread_func_resizecheckThread():
    global thread_variable_lastscreensize
    while (1):
        main()
        thread_variable_lastscreensize = [window.width(), window.height()]
        

window.setStyleSheet('QWidget{background-color:#0b0b0b;}')
window.show()
window.resize(600, 400)
window.setMinimumWidth(300)

main()

_thread.start_new_thread(thread_func_resizecheckThread, ())

application.exec_()
