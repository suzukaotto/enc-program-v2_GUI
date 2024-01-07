import src
import sys
import tkinter as tk
from tkinter import messagebox
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

menu1_str = "File Encryption"
menu2_str = "File Decryption"
menu3_str = "Program Exit"

github_icon = "program\src\icon\github.png"
program_icon = "program\src\icon\icon.png"

form_class = uic.loadUiType("program\src\MainMenuWindow.ui")[0]

class MainMenuWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.title_label.setText(src.program_title)
        self.menu1_btn.setText(menu1_str)
        self.menu2_btn.setText(menu2_str)
        self.menu3_btn.setText(menu3_str)
        
        self.menu1_btn.clicked.connect(self.menu1BtnClick)
        self.menu2_btn.clicked.connect(self.menu2BtnClick)
        self.menu3_btn.clicked.connect(self.menu3BtnClick)
        self.action_github.triggered.connect(self.githubActionClick)

        self.message_box = None
        self.select_menu_num = None


    def menu1BtnClick(self):
        print(f"File Enc")
        self.select_menu_num = 1
        
    def menu2BtnClick(self):
        print(f"File Dec")
        self.select_menu_num = 2

    def menu3BtnClick(self):
        print(f"Program Exit")
        
        self.close()
    
    def githubActionClick(self):
        open_url = QUrl("https://github.com/suzukaotto/enc-program-v2_GUI")
        QDesktopServices.openUrl(open_url)
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '프로그램 종료', '프로그램을 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            MainMenuWindow.select_menu_num = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainMenuWindow()
    myWindow.show()
    app.exec_()