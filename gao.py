import os
import shutil
import sys
import time

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                            QAction, qApp, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import youtube_dl


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                pass


        def my_hook(d):
            if d['status'] == 'finished':
                time.sleep(0.8)
                QMessageBox.question(self, 'Download', "Your download finished!",
                                    QMessageBox.Ok, QMessageBox.Ok)


        self.title = 'GAO'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 220
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }

        self.initUI()


    def initUI(self):
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        aboutAct = QAction('&About', self)
        aboutAct.setStatusTip('About')
        aboutAct.triggered.connect(self.about)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(aboutAct)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('icons/icon.png'))

        # Create the textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 80)
        self.textbox.resize(360, 30)

        # Create a button in the window
        self.button = QPushButton('Download', self)
        self.button.move(150, 130)

        # Connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()


    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([textboxValue])

        current_dir = os.getcwd()
        dir_name = 'audios'

        for file in os.listdir(path='.'):
            if file.endswith('.mp3'):
                audio_files = os.path.join(current_dir, file)
                audio_dir = os.path.join(current_dir, dir_name)
                shutil.move(audio_files, audio_dir)


    def about(self, event):
        reply = QMessageBox.question(self, 'Message',
                "                Name: GAO\n\
                Description: Extract audio from Youtube videos.\n\
                Version: 0.1.0\n\
                Author: Kennedy Allyson\n\
                Email: kennedy01101@gmail.com\n\
                Github: kennedyallyson",\
                QMessageBox.Yes, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            pass
        else:
            pass


def setup():
    if not os.path.exists('audios'):
        try:
            os.mkdir('audios')
        except e:
            print(e)


if __name__ == '__main__':
    setup()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
