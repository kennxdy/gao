import os
import shutil
import sys

from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton,
                            QAction, qApp, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon
import youtube_dl


class WorkerSignals(QObject):
    finished = pyqtSignal()


class Worker(QRunnable):
    def __init__(self, text, opts, label):
        super(QRunnable, self).__init__()
        self._text = text
        self._opts = opts
        self._label = label
        self.signals = WorkerSignals()


    def run(self):
        try:
            with youtube_dl.YoutubeDL(self._opts) as ydl:
                ydl.download([self._text])

            current_dir = os.getcwd()
            dir_name = 'audios'

            for file in os.listdir(path='.'):
                if file.endswith('.mp3'):
                    audio_files = os.path.join(current_dir, file)
                    audio_dir = os.path.join(current_dir, dir_name)
                    shutil.move(audio_files, audio_dir)
        except:
            print('An error has occurred')
        finally:
            self.signals.finished.emit()
            self._label.setText('')



class App(QMainWindow,):
    def __init__(self, parent=None):
        super(App, self).__init__()

        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                pass


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
        }

        self.initUI()


    def initUI(self):
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        aboutAct = QAction('About', self)
        aboutAct.triggered.connect(self.about)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAct)

        fileMenu = menubar.addMenu('Help')
        fileMenu.addAction(aboutAct)

        self.input_label = QLabel('VIDEO URL', self)
        self.input_label.move(163, 40)

        self.textbox = QLineEdit(self)
        self.textbox.move(50, 85)
        self.textbox.resize(300, 30)

        self.button = QPushButton('Download', self)
        self.button.move(150, 125)
        self.button.clicked.connect(self.on_click)

        self.info_label = QLabel('', self)
        self.info_label.move(10, 190)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('icons/icon.svg'))

        self.show()

        self.threadpool = QThreadPool()


    def thread_complete(self):
        QMessageBox.question(self, 'Download',
                            'Your download finished!',
                            QMessageBox.Ok, QMessageBox.Ok)


    @pyqtSlot()
    def on_click(self):
        text = self.textbox.text()

        if text == '':
            pass
        else:
            opts = self.ydl_opts
            self.info_label.setText('Downloading...')

            worker = Worker(text, opts, self.info_label)

            worker.signals.finished.connect(self.thread_complete)
            self.threadpool.start(worker)


    def about(self, event):
        reply = QMessageBox.question(self, 'About',
                '                Name: GAO\n\
                Description: Extract audio from Youtube videos\n\
                Version: 0.1.1\n\
                Author: Kennedy Allyson\n\
                Email: kennedy01101@gmail.com\n\
                Github: kennedyallyson',\
                QMessageBox.Ok, QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass
        else:
            pass


def setup():
    if not os.path.exists('audios'):
        try:
            os.mkdir('audios')
        except:
            pass


if __name__ == '__main__':
    setup()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
