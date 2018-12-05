#At this point, there is no way to save the result into an image file.

import PyQt5 as PyQt5
from PyQt5.QtWidgets import *
import sys as sys
import _thread as thread
import os as os

def event(eventType, debug = True):
    global applicationRunning
    eventType = str(eventType)
    if (debug):
        print (eventType)
    if (eventType == 'exitProgram'):
        applicationRunning = False
        exit()

applicationRunning = True

application = QApplication(sys.argv)

screen = application.primaryScreen()

window = QWidget()
window.setWindowTitle('Paint')
window.setStyleSheet('QWidget{background-color:white;}')
window.setMinimumSize(500, 300)
window.setWindowIcon(PyQt5.QtGui.QIcon('paint_application_icon.png'))
window.resize((screen.size().width() / 2), (screen.size().height() / 2))

window_header_bar = QMenuBar(window)
window_header_bar.resize(window.width(), 20)

window_header_bar_widgetStyleSheet = '''
QMenu{background-color:lightgray;border:1px solid #636361;color:black;font-family:Calibri;font-size:13px;}
'''

window_header_bar_widgets_file = window_header_bar.addMenu('File')
window_header_bar_widgets_file.setGeometry(0, 0, 40, 20)
window_header_bar_widgets_file.setStyleSheet(window_header_bar_widgetStyleSheet)
window_header_bar_widgets_file.addAction('New').triggered.connect(lambda: event('canvasClear'))
window_header_bar_widgets_file.addAction('Open').triggered.connect(lambda: event('canvasOpenFile'))
window_header_bar_widgets_file.addAction('Exit').triggered.connect(lambda: event('exitProgram'))

window_header_bar_widgets_edit = window_header_bar.addMenu('Edit')
window_header_bar_widgets_edit.setGeometry((window_header_bar_widgets_file.x() + window_header_bar_widgets_file.width()), 0, 40, 20)
window_header_bar_widgets_edit.setStyleSheet(window_header_bar_widgetStyleSheet)

window_header_bar_widgets_edit_new_brush = window_header_bar_widgets_edit.addMenu('Brush')

window_header_bar_widgets_edit_new_brush_color = window_header_bar_widgets_edit_new_brush.addMenu('Set Color...')
window_header_bar_widgets_edit_new_brush_color.addAction('Black').triggered.connect(lambda: event('setcolor:black'))
window_header_bar_widgets_edit_new_brush_color.addAction('Gray').triggered.connect(lambda: event('setcolor:gray'))
window_header_bar_widgets_edit_new_brush_color.addAction('White').triggered.connect(lambda: event('setcolor:white'))
window_header_bar_widgets_edit_new_brush_color.addAction('Blue').triggered.connect(lambda: event('setcolor:blue'))
window_header_bar_widgets_edit_new_brush_color.addAction('Orange').triggered.connect(lambda: event('setcolor:orange'))
window_header_bar_widgets_edit_new_brush_color.addAction('Red').triggered.connect(lambda: event('setcolor:red'))
window_header_bar_widgets_edit_new_brush_color.addAction('Purple').triggered.connect(lambda: event('setcolor:purple'))
window_header_bar_widgets_edit_new_brush_color.addAction('Yellow').triggered.connect(lambda: event('setcolor:yellow'))

pencolor = 'black'
pen = PyQt5.QtGui.QPen(eval('PyQt5.QtCore.Qt.{}'.format(pencolor)), 2, PyQt5.QtCore.Qt.SolidLine)

def paintEvent(x1, y1, x2, y2):
    global renderView
    hwh = window.height() // 2
    hww = window.width() // 2
    x1 -= hww
    x2 -= hww
    y1 -= hwh
    y2 -= hwh
    a = QGraphicsLineItem(PyQt5.QtCore.QLineF(x1, y1, x2, y2))
    renderView.scene().addItem(a)
    print (x1, y1, x2, y2)

renderView = QGraphicsView(window)
renderView.move(0, window_header_bar.height())
renderView.setScene(QGraphicsScene(window))
renderView.setSceneRect(PyQt5.QtCore.QRectF(renderView.viewport().rect()))

downpos = ''

def mouseDown(c):
    global downpos
    if (downpos == ''):
        downpos = c
    paintEvent(downpos[0], downpos[1], c[0], c[1])
    downpos = c

window.mousePressEvent = lambda e: mouseDown((e.x(), e.y()))

def resizeThread():
    global applicationRunning
    while (applicationRunning):
        window_header_bar.resize(window.width(), 20)
        renderView.resize(window.width(), (window.height() - window_header_bar.height()))

thread.start_new_thread(resizeThread, ())

window.show()

application.exec_()

applicationRunning = False

#I got fed up with QPainter so I didnt use it        ;-;