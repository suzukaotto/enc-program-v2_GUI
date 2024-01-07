from src.src import *
from src.windows import *
import os, json, base64
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import tkinter
from tkinter import messagebox

def enc_file():
    global end_sign, program_title
    program_title_local = (program_title + " - Encrypting")
    
    # File select
    print(f"File selecting...")
    org_file_path = file_select()
    if org_file_path == None:
        return 1
    print(f"Selected File: {org_file_path}")
    
    # Check file extension
    if ("."+get_file_extension(org_file_path)) == file_extension:
        print("incorrect extension")
        messagebox.showwarning(title=program_title_local, message="This extension cannot be encrypted.")
        return 1

    # File data load
    print("Select File Data Load...")
    with open(org_file_path, "rb") as file_read_data:
        file_data = file_read_data.read()
    print("Select File Data Load Complit")
    ## org file name save
    file_data_json = f'{{"file_name":"{get_filename_from_path(org_file_path)}"}}'
    file_data_json = json.loads(file_data_json)
    
    # password Setting
    print("Password setting...")
    print("Enter the password you want to use for the file")
    try:
        user_input_pw = input(">> ")
    except KeyboardInterrupt:
        return 1

    ## password save
    user_input_pw_hashed = str_hashing(user_input_pw, str_hashing(user_input_pw, str_hashing(user_input_pw)))
    file_data_json["file_pw"] = user_input_pw_hashed.decode('utf-8')
    print("Password setted")
    
    # File org data ENC
    print("File org data Encrypting...")
    ## Password Key Generate
    file_enc_key = user_input_pw_hashed
    encFernet = Fernet(file_enc_key)
    file_enc_data = encFernet.encrypt(file_data)
    ## Delete password, key
    user_input_pw = None
    file_enc_key = None
    print("File org data Encrypted")

    # File data Combination
    print("File data Combination...")
    file_data_json = json.dumps(file_data_json).encode('utf-8')
    combined_file_data = file_data_json + end_sign + file_enc_data
    print("File data Combinated")

    # base64 incoding
    print("base64 incoding...")
    combined_file_data_base64_encd = base64.b64encode(combined_file_data)
    print("base64 incoded")
    
    # File name check
    print(f"Check file name...")
    file_save_path = remove_extension(org_file_path) + file_extension
    while True:
        if not check_validate_file_name(file_save_path):
            print("Invalid file name")
            if not messagebox.askokcancel(title=program_title_local, message=f"{file_save_path}\n\nFile name not allowed.\nPlease enter again.\nIf you cancel, all progress will be cancelled."):
                return 1
            print("new Save file name input")
            file_save_path = remove_filename_from_path(org_file_path) + os.sep + input(">> ") + file_extension
            continue
        elif check_duplicate_file(file_save_path):
            print("There is a file with the same name in that path")
            if not messagebox.askokcancel(title=program_title_local, message=f"{file_save_path}\n\nThere is a file with a duplicate name in the path.\nDo you want to overwrite?"):
                if not messagebox.askokcancel(title=program_title_local, message=f"{file_save_path}\n\nChange the file name to be saved.\nIf you cancel, all progress will be cancelled."):
                    return 1
            else:
                break
            print("new Save file name input")
            file_save_path = remove_filename_from_path(org_file_path) + os.sep + input(">> ") + file_extension
            continue

        # When there is no problem
        break
    print(f"File name check completed")

    # File Save
    print("File Saving...")
    try:
        with open(file_save_path, "wb") as file_write_data:
            file_write_data.write(combined_file_data_base64_encd)
    except Exception as e:
        print(f"An error occurred while saving: {e}")
        print(f"Please try again from the beginning.")
        return 2
    print(f"File Saved: [{file_save_path}]")

    # org File delete
    print("deleting org file...")
    delete_file(org_file_path)

    # task complite
    print("File encrypting success")
    return 0
    
def dec_file():
    global program_title
    program_title_local = (program_title + " - Decrypting")

    # File select
    print(f"File selecting...")
    org_file_path = file_select()
    if org_file_path == None:
        return 1
    print(f"Selected File: {org_file_path}")

    # Check file extension
    if ("."+get_file_extension(org_file_path)) != file_extension:
        print("incorrect extension")
        messagebox.showwarning(title=program_title_local, message="This extension cannot be decrypted.")
        return 1

    # File data extract
    print("File data extracting...")
    file_data_extract_data = file_data_extract(org_file_path)
    if file_data_extract_data == 2:
        return 2
    elif file_data_extract_data == 4:
        return 4
    
    try:
        file_info_data_json = json.loads(file_data_extract_data[0].decode('utf-8'))
        org_file_data = file_data_extract_data[1]
        org_file_name = file_info_data_json['file_name']
        file_pw = file_info_data_json['file_pw']
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        return 2
    print("File data extracted")

    # org File data dec
    print("Entering password...")
    ## input pw
    print("Enter the password you want to use for the file")
    try:
        user_input_pw = input(">> ")
    except KeyboardInterrupt:
        return 1
    print("Password entered")
    
    ## dec data
    print("File data Decrypting...")
    try:
        file_dec_key = str_hashing(user_input_pw, str_hashing(user_input_pw, str_hashing(user_input_pw)))
        decFernet = Fernet(file_dec_key)
        deced_org_file_data = decFernet.decrypt(org_file_data)
    except InvalidToken:
        return 3
    except Exception as e:
        print(f"An error occurred: {e}")
        return 2
    print("File data Decrypted.")

    # File name check
    print(f"Check file name...")
    file_save_path = remove_filename_from_path(org_file_path) + os.sep + org_file_name
    print(file_save_path)
    while True:
        if not check_validate_file_name(file_save_path):
            print("Invalid file name")
            if not messagebox.askokcancel(title=program_title_local, message=f"{file_save_path}\n\nFile name not allowed.\nPlease enter again.\nIf you cancel, all progress will be cancelled."):
                return 1
            print("new Save file name input")
            file_save_path = remove_filename_from_path(org_file_path) + os.sep + input(">> ") + file_extension
            continue
        elif check_duplicate_file(file_save_path):
            print("There is a file with the same name in that path")
            if not messagebox.askokcancel(title=program_title_local, message=f"{file_save_path}\n\nThere is a file with a duplicate name in the path.\nDo you want to overwrite?"):
                if not messagebox.askokcancel(title=program_title_local, message=f"{file_save_path}\n\nChange the file name to be saved.\nIf you cancel, all progress will be cancelled."):
                    return 1
            else:
                break
            print("new Save file name input")
            file_save_path = remove_filename_from_path(org_file_path) + os.sep + input(">> ") + file_extension
            continue

        # When there is no problem
        break
    print(f"File name check completed")

    # File Save
    print("File Saving...")
    try:
        with open(file_save_path, "wb") as file_write_data:
            file_write_data.write(deced_org_file_data)
    except Exception as e:
        print(f"An error occurred while saving: {e}")
        print(f"Please try again from the beginning.")
        return 2
    print(f"File Saved: [{file_save_path}]")
    
    # org File delete
    print("deleting org file...")
    delete_file(org_file_path)

    # task complit
    print("File encryption success")
    return 0

    
def program_exit():
    global program_title
    program_title_local = (program_title + " - Exit")

    if messagebox.askokcancel(title=program_title_local, message="Are you sure you want to quit the program?"):
        print('Program exit')
        exit(0)
    else:
        return 1

class mainWindow:
    def __init__(self):
        self.root = tkinter.Tk()
        self.create_window()

    def create_window(self):
        label = tkinter.Label(self.root, text="라벨")
        label.pack()

        button1 = tkinter.Button(self.root, text="버튼 1", command=self.button1_func)
        button1.pack()

        button2 = tkinter.Button(self.root, text="버튼 2", command=self.button2_func)
        button2.pack()

        button3 = tkinter.Button(self.root, text="버튼 3", command=self.button3_func)
        button3.pack()

    def button1_func(self):
        print("button1")

    def button2_func(self):
        print("button2")

    def button3_func(self):
        print("button3")

    def run(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    app = MenuSelectionWindow(root)
    root.mainloop()

    sel_num = app.select_menu_num

    if sel_num == 1:
        enc_result = enc_file()
        
        if enc_result == 0:
            print("Encrypted successfully.")
            messagebox.showinfo(title=program_title, message="Encrypted successfully.")
        elif enc_result == 1:
            print("Encryption has been cancelled.")
            messagebox.showwarning(title=program_title, message="Encryption has been cancelled.")
        elif enc_result == 2:
            print("Encryption was canceled because an error occurred.")
            messagebox.showerror(title=program_title, message="Encryption was canceled because an error occurred.\nPlease try again from the beginning.")
    
    elif sel_num == 2:
        dec_result = dec_file()
    
        if dec_result == 0:
            print("Decrypted successfully.")
            messagebox.showinfo(title=program_title, message="Decrypted successfully.")
        elif dec_result == 1:
            print("Decryption has been cancelled.")
            messagebox.showwarning(title=program_title, message="Decryption has been cancelled.")
        elif dec_result == 2:
            print("Decryption was canceled because an error occurred.")
            messagebox.showerror(title=program_title, message="Decryption was canceled because an error occurred.\nPlease try again from the beginning.")
        elif dec_result == 3:
            print("Please check your password again.")
            messagebox.showwarning(title=program_title, message="Please check your password again.\nPlease try again from the beginning.")
        elif dec_result == 4:
            print("This is not a valid file.")
            messagebox.showwarning(title=program_title, message="This is not a valid file.\nPlease try again from the beginning.")
        
    elif sel_num == 3:
        exit_result = program_exit()

        if exit_result == 1:
            print("Program exit canceled")
        
    else:
        return 1
    
    return 0

while True:
    main_result = main()