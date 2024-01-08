from src.windows import *
from src.src import *

import sys
from PyQt5.QtWidgets import QApplication

def main():
    QApp = QApplication(sys.argv)
    MainMenuClass = MainMenuWindow()

    while True:
        # Main Menu Page
        MainMenuClass.show()
        QApp.exec_()

        if MainMenuClass.select_menu_num == 1:
            # File Enc Page
            FileEncClass = FileEncWindow()
            FileEncClass.show()
            QApp.exec_()
        
        elif MainMenuClass.select_menu_num == 2:
            # File Dec Page
            FileDecClass = FileDecWindow()
            FileDecClass.show()
            QApp.exec_()

        MainMenuClass.select_menu_num == None

main()