from src import src
import os
from tkinterdnd2 import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt, QUrl, QFileInfo
from PyQt5.QtGui import QDesktopServices, QDragEnterEvent, QDropEvent

github_icon = "program\src\icon\github.png"
program_icon = "program\src\icon\icon.png"

class FileDecWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("program/src/FileDecWindow.ui", self)

        self.setWindowTitle(src.program_title)
        self.ui.title_label.setText("File Decryption")

        # back btn
        self.ui.back_btn.clicked.connect(self.back_btn_clicked)
        
        # file select
        self.ui.file_select_label.setAcceptDrops(True)
        self.ui.file_select_label.dragEnterEvent = self.drag_enter_event
        self.ui.file_select_label.dropEvent = self.drop_event
        self.ui.file_select_label.setStyleSheet("background-color: #dbdbdb; color: #000000; border-radius: 5px;")
        self.ui.file_select_btn.clicked.connect(self.file_select)
        self.select_file_path = None

        # file dec btn
        self.ui.file_dec_btn.clicked.connect(self.dec_file)
        self.dec_btn_manager()
        
        # progress bar
        self.update_progress(0)
        self.dec_working = False
        self.dec_result = 0

    def dec_file(self):
        self.setWindowTitle(src.program_title + " - Decrypting...")
        self.dec_working = True
        self.ui_setEnabled(False)
        
        # enc_task
        try:
            dec_result = src.dec_file(self.select_file_path, self.ui.pw_entry.text(), self.update_progress)
        except Exception as e:
            print(f"An unknown error occurred during encryption: {e}")
            dec_result = 2

        if dec_result == 4:
            print("Decryption was canceled because no identifier was found in the file (the program was not decrypting the file).")
            QMessageBox.warning(self, src.program_title, f"No identifier found in file.\nCheck whether the file is encrypted with [{src.program_title}].")

        elif dec_result == 4:
            print("This extension does not support decryption.")
            QMessageBox.warning(self, src.program_title, f"This extension does not support decryption.\nPlease select a file with the [{src.file_extension}] extension.")
        elif dec_result == 3:
            print("Decryption was canceled because the file password was incorrect.")
            QMessageBox.critical(self, src.program_title, "The file password is incorrect.\nPlease check the file password and re-enter it.")
        elif dec_result == 2:
            print("Decryption canceled due to error")
            QMessageBox.critical(self, src.program_title, "An unknown error occurred during decryption.\nPlease try again from the beginning.")
        elif dec_result == 1:
            print("Decryption canceled")
            QMessageBox.warning(self, src.program_title, "Decryption has been cancelled.")
        elif dec_result[0] == 0:
            print("Decryption Success")
            QMessageBox.information(self, src.program_title, f"The file has been successfully decrypted.\n{dec_result[1]}")
        
        # restoration
        self.setWindowTitle(src.program_title)
        self.dec_working = False
        self.ui_setEnabled(True)
        self.update_progress(0, "normal")

    def dec_btn_manager(self):
        if self.select_file_path != None:
            self.file_dec_btn.setText("File Decryption")
            self.file_dec_btn.setEnabled(True)
        
        else:
            self.ui.file_dec_btn.setEnabled(False)

            if self.select_file_path == None:
                self.ui.file_dec_btn.setText("Select a file")

    def ui_setEnabled(self, activate:bool):
        # file select enabled
        self.ui.file_select_label.setEnabled(activate)
        self.ui.file_select_btn.setEnabled(activate)
        
        # pw entry enabled
        self.ui.pw_entry.setReadOnly(not activate)
        
        # enc btn enabled
        self.ui.file_dec_btn.setVisible(activate)

        # progress bar enabled
        self.ui.progress_bar.setEnabled(not activate)

    def update_progress(self, value: int = None, status: str = "normal"):
        status = status.lower()
        if status == "normal":
            self.ui.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        elif status == "warning":
            self.ui.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
        elif status == "error":
            self.ui.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")

        # set value
        if value == None: return
        self.ui.progress_bar.setValue(value)

    def selected_file_path_save(self, file_path):
        if file_path == None:
            return
        
        self.select_file_path = file_path
        
        self.ui.file_select_label.setText(self.select_file_path)
        self.ui.file_select_label.setToolTip(self.select_file_path)
        self.ui.file_select_label.setStyleSheet("background-color: #c2c2c2; color: #000000; border-radius: 5px;")

        self.dec_btn_manager()
    
    def file_select(self):
        self.selected_file_path_save(src.file_select())
        
    def drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event: QDropEvent):
        urls = event.mimeData().urls()
        files = []
        for url in urls:
            file_path = url.toLocalFile()
            if QFileInfo(file_path).isFile():
                files.append(file_path)

        if files:
            self.selected_file_path_save(files[0])
    
    def back_btn_clicked(self):
        self.close()

    def show_dialog(self, title="", message=""):
        reply = QMessageBox.question(self, title, message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False


    def closeEvent(self, event):
        if self.dec_working == True:
            print("Decrypting... Close event rejected.")
            event.ignore()
            return

        reply = QMessageBox.question(self, src.program_title, 'All entered information will be lost.\nWould you like to return to the menu?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            print("File Encryption window exited")
        else:
            event.ignore()
            print("File Encryption window exit canceled")





class FileEncWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("program/src/FileEncWindow.ui", self)

        self.setWindowTitle(src.program_title)
        self.ui.title_label.setText("File Encryption")

        self.ui_setEnabled(True)

        # back btn
        self.ui.back_btn.clicked.connect(self.back_btn_clicked)
        
        # file select
        self.ui.file_select_label.setAcceptDrops(True)
        self.ui.file_select_label.dragEnterEvent = self.drag_enter_event
        self.ui.file_select_label.dropEvent = self.drop_event
        self.ui.file_select_label.setStyleSheet("background-color: #dbdbdb; color: #000000; border-radius: 5px;")
        self.ui.file_select_btn.clicked.connect(self.file_select)
        self.select_file_path = None
        
        # password entry
        self.ui.pw_entry.textChanged.connect(self.check_password_match)
        self.ui.pw_cf_entry.textChanged.connect(self.check_password_match)
        self.user_input_pw = ""
        self.password_valid = True
        
        # check box
        self.ui.check_box.stateChanged.connect(self.check_box_clicked)
        self.check_box_valid = False
        
        # file enc btn
        # self.ui.file_enc_btn.setStyleSheet("background-color: #CCCCCC;")
        self.ui.file_enc_btn.clicked.connect(self.file_enc)
        self.enc_btn_manager()
        
        # progress bar
        self.update_progress(0)
        self.enc_working = False
        self.enc_result = 0
        
    
    
    def file_enc(self):
        self.setWindowTitle(src.program_title + " - Encrypting...")
        self.enc_working = True
        self.ui_setEnabled(False)
        
        # enc_task
        try:
            enc_result = src.enc_file(self.select_file_path, self.user_input_pw, self.update_progress)
        except Exception as e:
            print(f"An unknown error occurred during encryption: {e}")
            enc_result = 2

        if enc_result == 3:
            print("Encryption was canceled because the extension was incorrect.")
            QMessageBox.warning(self, src.program_title, f"This extension cannot be encrypted.\nPlease select a file that does not have the [{src.file_extension}] extension.")
        elif enc_result == 2:
            print("Encryption canceled due to error")
            QMessageBox.critical(self, src.program_title, "An unknown error occurred during encryption.\nPlease try again from the beginning.")
        elif enc_result == 1:
            print("Encryption canceled")
            QMessageBox.warning(self, src.program_title, "Encryption has been cancelled.")
        elif enc_result[0] == 0:
            print("Encryption Success")
            QMessageBox.information(self, src.program_title, f"The file has been successfully encrypted.\n{enc_result[1]}")
        
        # restoration
        self.setWindowTitle(src.program_title)
        self.enc_working = False
        self.ui_setEnabled(True)
        self.update_progress(0, "normal")

    def ui_setEnabled(self, activate:bool):
        # file select enabled
        self.ui.file_select_label.setEnabled(activate)
        self.ui.file_select_btn.setEnabled(activate)
        
        # pw entry enabled
        self.ui.pw_entry.setReadOnly(not activate)
        self.ui.pw_cf_entry.setReadOnly(not activate)

        # check box enabled
        self.ui.check_box.setEnabled(activate)
        
        # enc btn enabled
        self.ui.file_enc_btn.setVisible(activate)

        # progress bar enabled
        self.ui.progress_bar.setEnabled(not activate)

    def update_progress(self, value: int = None, status: str = "normal"):
        if status == "normal":
            self.ui.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        elif status == "warning":
            self.ui.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
        elif status == "error":
            self.ui.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")

        # set value
        if value == None: return
        self.ui.progress_bar.setValue(value)
    
    def enc_btn_manager(self):
        if (self.select_file_path != None) and self.password_valid and self.check_box_valid:
            self.ui.file_enc_btn.setText("File Encryption")
            self.ui.file_enc_btn.setEnabled(True)
        else:
            self.ui.file_enc_btn.setEnabled(False)
            
            if self.check_box_valid == False:
                self.ui.file_enc_btn.setText("Click the checkbox")
            
            if self.password_valid == False:
                self.ui.file_enc_btn.setText("Check your password")
                
            if self.select_file_path == None:
                self.ui.file_enc_btn.setText("Select a file")
    
    def enc_check_box_manager(self):
        if self.password_valid:
            self.check_box.setEnabled(True)
        else:
            self.check_box.setEnabled(False)
            self.check_box.setChecked(False)
        

    def check_password_match(self):
        pw_text = self.ui.pw_entry.text()
        pw_cf_text = self.ui.pw_cf_entry.text()

        if pw_text == pw_cf_text:
            self.password_valid = True
            self.user_input_pw = pw_text
        else:
            self.password_valid = False

        self.enc_btn_manager()
        self.enc_check_box_manager()
        
    def check_box_clicked(self, state):
        if state == Qt.Checked:
            self.check_box_valid = True
        else:
            self.check_box_valid = False
        
        self.enc_btn_manager()
    
    def back_btn_clicked(self):
        self.close()
    
    def selected_file_path_save(self, file_path):
        if file_path == None:
            return
        
        self.select_file_path = file_path
        
        self.ui.file_select_label.setText(self.select_file_path)
        self.ui.file_select_label.setToolTip(self.select_file_path)
        self.ui.file_select_label.setStyleSheet("background-color: #c2c2c2; color: #000000; border-radius: 5px;")
        self.enc_btn_manager()
    
    def file_select(self):        
        self.selected_file_path_save(src.file_select())
        
    def drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event: QDropEvent):
        urls = event.mimeData().urls()
        files = []
        for url in urls:
            file_path = url.toLocalFile()
            if QFileInfo(file_path).isFile():  # 파일인지 확인
                files.append(file_path)

        if files:
            self.selected_file_path_save(files[0])
    
    def closeEvent(self, event):
        if self.enc_working == True:
            event.ignore()
            print("Encrypting... Close event rejected.")
            return

        reply = QMessageBox.question(self, src.program_title, 'All entered information will be lost.\nWould you like to return to the menu?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            print("File Encryption window exited")
        else:
            event.ignore()
            print("File Encryption window exit canceled")


class MainMenuWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = uic.loadUi("program/src/MainMenuWindow.ui", self)
        
        self.setWindowTitle(src.program_title)
        self.title_label.setText(src.program_title)
        self.sub_title_label.setText(src.program_sub_title)
        
        self.menu1_btn.clicked.connect(self.menu1BtnClick)
        self.menu2_btn.clicked.connect(self.menu2BtnClick)
        self.menu3_btn.clicked.connect(self.menu3BtnClick)
        self.action_github.triggered.connect(self.githubActionClick)

        self.message_box = None
        self.select_menu_num = None


    def menu1BtnClick(self) -> None:
        print(f"Move to File Encrypting Page..")
        self.select_menu_num = 1
        self.close()
        
    def menu2BtnClick(self) -> None:
        print(f"Move to File Decrypting Page..")
        self.select_menu_num = 2
        self.close()

    def menu3BtnClick(self) -> None:
        print(f"Program Exiting...")
        self.select_menu_num = None
        self.close()
    
    def githubActionClick(self) -> None:
        open_url = "https://github.com/suzukaotto/enc-program-v2_GUI"
        QDesktopServices.openUrl(QUrl(open_url))
        print("github page opened")
    
    def closeEvent(self, event):
        if self.select_menu_num != None:
            self.close()
            return
        
        reply = QMessageBox.question(self, src.program_title, 'Are you sure you want to quit the program?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            print("Program Exted")
            exit(0)
        else:
            event.ignore()
            print("Program Exit Canceled")