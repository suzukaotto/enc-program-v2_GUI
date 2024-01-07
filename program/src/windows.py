from src import *
import sys
import tkinter as tk
from tkinter import messagebox
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

github_icon = "program\src\icon\github.png"
program_icon = "program\src\icon\icon.png"

form_class = uic.loadUiType("program\src\MainMenuWindow.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.menu1_btn.clicked.connect(self.menu1BtnClick)
        self.menu2_btn.clicked.connect(self.menu2BtnClick)
        self.menu3_btn.clicked.connect(self.menu3BtnClick)
        self.action_github.triggered.connect(self.githubActionClick)

    def menu1BtnClick(self):
        print(f"File Enc")
    def menu2BtnClick(self):
        print(f"File Dec")
    def menu3BtnClick(self):
        print(f"Program Exit")
    def githubActionClick(self):
        open_url = QUrl("https://github.com/suzukaotto/enc-program-v2_GUI")
        QDesktopServices.openUrl(open_url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()