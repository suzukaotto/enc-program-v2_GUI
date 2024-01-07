import os, json, re, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken
from tkinter import filedialog
from tkinter import messagebox

program_title = "File Guardian"

end_sign = b"IF_YOU_EDIT_THE_ABOVE_DATA " + bytes([0xFE, 0xEF, 0xFA, 0xCE]) + b"THE_FILE_MAY_NOT_BE_DECRYPTCRY_PROPERLY"
file_extension = ".fgef"

def cls():
    os.system("cls")

def pause():
    os.system("pause")

def console_dialog():
    while True:
        try:
            user_input = input(" (Y/N): ").strip().lower()
        except KeyboardInterrupt:
            print("Canceled")
            return 2
        
        if user_input in ['y', 'n']:
            return True if user_input == 'y' else False
        else:
            print("Please enter Y or N.")

def select_folder():
    global program_title
    program_title_local = (program_title + " - Folder Select")

    while True:
        folder_path = filedialog.askdirectory(title=program_title_local)
        
        if folder_path == '':
            if messagebox.askyesno(title=program_title_local, message="Please select a folder."):
                continue
            else:
                return None
        
        if messagebox.askyesno(title=program_title_local, message=f"{folder_path}\n\nWould you like to select this folder?"):
            return folder_path
        else :
            continue

def file_select():
    global program_title
    program_title_local = (program_title + " - File select")

    while True:
        file_path = filedialog.askopenfilename(title=program_title_local)

        if file_path == '':
            if messagebox.askokcancel(title=program_title_local, message="Please select a file."):
                continue
            else:
                return None
        
        if messagebox.askokcancel(title=program_title_local, message=f"{file_path}\nDo you want to continue?"):
            return file_path
        else:
            continue

def files_select():
    global program_title
    program_title_local = (program_title + " - File select")

    while True:
        file_paths = filedialog.askopenfilenames(title=program_title_local)

        if file_paths == '':
            if messagebox.askokcancel(title=program_title_local, message="Please select a file."):
                continue
            else:
                return None
        
        file_path_msg = ''
        if len(file_paths) >= 30:
            file_path_msg = f"There are too many selected files to display. ({len(file_paths)})\n"
        else:
            for file_path_tuple in file_paths:
                file_path_msg += str(file_path_tuple) + "\n"
        
        if messagebox.askokcancel(title=program_title_local, message=f"{file_path_msg}\nDo you want to continue?"):
            return file_paths
        else :
            continue

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File deleted: [{file_path}]")
    except OSError as e:
        print(f"File deletion failed: [{file_path}] {e.strerror}")

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def check_duplicate_file(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False

def remove_extension(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    return file_name

def remove_filename_from_path(path):
    directory, filename = os.path.split(path)
    return directory

def get_filename_from_path(file_path):
    return os.path.basename(file_path)

def get_file_extension(file_path):
    split_path = file_path.split('.')
    
    if len(split_path) == 1 or split_path[-1] == '':
        return 1
    
    file_extension = split_path[-1]
    return file_extension

def file_data_extract(file_path):
    global end_sign
    
    try:
        with open(file_path, 'rb') as file_data:
            data = file_data.read()

            # base64 decode
            data = base64.b64decode(data)
            
            index = data.find(end_sign)
            if index != -1:
                data_after_sign = data[:index]
                data_before_sign = data[index + len(end_sign):]
                return (data_after_sign, data_before_sign)
            else:
                print("End sign not found in the file data")
                return 4

    except Exception as e:
        print(f"An error occurred: {e}")
        return 2

def check_valid_password(input_string):
    min_len = 1
    max_len = 512
    regex   = r'^[a-zA-Z0-9!@#$%^&*()-_=+[\]{};:\'",.<>/?\\|`~]*$'
    
    if min_len > len(input_string):
        return "The password you entered is too short."
    elif max_len < len(input_string):
        return "The password you entered is too long"
    
    pattern = re.compile(regex)
    if bool(pattern.match(input_string)):
        return True
    else:
        return "An illegal character is included."

def check_validate_file_name(file_path):
    file_name_pattern = r'[^\\/:*?"<>|\r\n]+$'
    file_name_match = re.search(file_name_pattern, file_path)
    
    if file_name_match:
        extracted_file_name = file_name_match.group()
        
        invalid_chars = r'[\/:*?"<>|]'
        reserved_words = r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$'
        
        valid_file_name = r'^[^\/:*?"<>|]*$'
        
        if (
            re.match(valid_file_name, extracted_file_name) and 
            not re.search(invalid_chars, extracted_file_name) and
            not re.match(reserved_words, extracted_file_name, re.IGNORECASE)
        ):
            return True
        else:
            return False
    else:
        messagebox.showinfo("The file name could not be extracted.")
        return False

def str_hashing(password, salt=b'salt', iterations=100_000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)