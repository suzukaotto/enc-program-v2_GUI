import os, json, re, base64
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PyQt5.QtWidgets import QMessageBox
from tkinter import filedialog
from tkinter import messagebox

program_title = "File Guardian"
program_version = "2.0"
program_sub_title = "Provides strong encryption capabilities."

file_identifier = b"IF_YOU_EDIT_THE_ABOVE_DATA " + bytes([0xFE, 0xEF, 0xFA, 0xCE]) + b"THE_FILE_MAY_NOT_BE_DECRYPTCRY_PROPERLY"
file_extension = ".fgef"

def enc_file(file_path, file_password, update_progress):
    """
    0 = Encryption completed
    1 = Cancel decryption operation
    2 = An unknown error occurred
    3 = This extension cannot be encrypted.
    """

    global file_identifier, program_title
    program_title_local = (program_title + " - Encryption Func")

    update_progress(0)
    
    # File select
    print(f"Selected File: {file_path}")
    update_progress(5)
    

    # Check file extension
    if ("."+get_file_extension(file_path)) == file_extension:
        update_progress(status="warning")
        return 3
    update_progress(10)

    # File data load and task
    try:
        ## File data load
        print("Select File Data Load...")
        with open(file_path, "rb") as file_read_data:
            file_data = file_read_data.read()
        print("Select File Data Load Complit")
        update_progress(20)

        ## org file name save
        file_data_json = f'{{"file_name":"{get_filename_from_path(file_path)}"}}'
        file_data_json = json.loads(file_data_json)
        update_progress(25)

    except Exception as e:
        print(f"An unknown error occurred while loading the file: {e}")
        update_progress(status="error")
        return 2
    
    # password Setting
    print("Password setting...")
    file_password_hashed = str_hashing(file_password, str_hashing(file_password, str_hashing(file_password, str_hashing(file_password))))
    print("Password setted")
    update_progress(30)
    
    # File org data ENC
    print("File org data Encrypting...")
    ## Password Key Generate
    file_enc_key = file_password_hashed
    encFernet = Fernet(file_enc_key)
    file_enc_data = encFernet.encrypt(file_data)
    update_progress(45)
    ## Memory Delete password, key
    for i in range(50+1):
        file_password = Fernet.generate_key()
        file_enc_key = Fernet.generate_key()
    print("File org data Encrypted")
    update_progress(50)

    # File data Combination
    print("File data Combination...")
    file_data_json = json.dumps(file_data_json).encode('utf-8')
    combined_file_data = file_data_json + file_identifier + file_enc_data
    print("File data Combinated")
    update_progress(65)

    # base64 incoding
    print("base64 incoding...")
    combined_file_data_base64_encd = base64.b64encode(combined_file_data)
    print("base64 incoded")
    update_progress(80)
    
    # File name check
    print(f"Check file name...")
    file_save_path = remove_extension(file_path) + file_extension
    
    if check_duplicate_file(file_save_path):
        print("There is a file with the same name in that path")
        update_progress(status="warning")
        if QMessageBox.warning(None, program_title_local, f"{file_save_path}\n\nThere is a file with a duplicate name in the path.\nDo you want to overwrite?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            file_save_path = get_non_duplicate_filename(file_save_path)
            if QMessageBox.warning(None, program_title_local, f"{file_save_path}\n\nWould you like to save it with the name above?\nIf you select No, all progress will be cancelled.", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return 1

    print(f"File name check completed")
    update_progress(85)

    # File Save
    print("File Saving...")
    try:
        with open(file_save_path, "wb") as file_write_data:
            file_write_data.write(combined_file_data_base64_encd)
    except Exception as e:
        print(f"An error occurred while saving: {e}")
        print(f"Please try again from the beginning.")
        update_progress(status="error")
        return 2
    print(f"File Saved: [{file_save_path}]")
    update_progress(100)

    # task complite
    print("File encrypting success")
    return [0, file_save_path]
    
def dec_file(file_path, file_password, update_progress):
    """
    0 = Decryption completed
    1 = Cancel decryption operation
    2 = An unknown error occurred
    3 = File password incorrect
    4 = Identifier not found (not the program's encryption method)
    """

    global program_title
    program_title_local = (program_title + " - Decryption Func")

    # File select
    print(f"File selecting...")
    org_file_path = file_path
    update_progress(5)
    print(f"Selected File: {org_file_path}")

    # Check file extension
    if ("."+get_file_extension(org_file_path)) != file_extension:
        update_progress(status="wawrning")
        return 4
    update_progress(10)

    # File data extract
    print("File data extracting...")
    file_data_extract_data = file_data_extract(org_file_path)
    if file_data_extract_data == 2:
        update_progress(status="error")
        return 2
    elif file_data_extract_data == 4:
        update_progress(status="warning")
        return 4
    update_progress(50)
    
    try:
        file_info_data_json = json.loads(file_data_extract_data[0].decode('utf-8'))
        org_file_data = file_data_extract_data[1]
        org_file_name = file_info_data_json['file_name']
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        update_progress(status="error")
        return 2
    update_progress(60)
    print("File data extracted")

    # org File data dec
    print("Entering password...")
    user_input_pw = file_password
    update_progress(65)
    print("Password entered")
    
    ## dec data
    print("File data Decrypting...")
    try:
        file_dec_key = str_hashing(user_input_pw, str_hashing(user_input_pw, str_hashing(user_input_pw, str_hashing(user_input_pw))))
        decFernet = Fernet(file_dec_key)
        deced_org_file_data = decFernet.decrypt(org_file_data)
    except InvalidToken:
        update_progress(status="warning")
        return 3
    except Exception as e:
        print(f"An error occurred: {e}")
        update_progress(status="error")
        return 2
    update_progress(90)
    print("File data Decrypted.")

    # save File name check
    print(f"Check file name...")
    file_save_path = remove_filename_from_path(org_file_path) + os.sep + org_file_name
    
    if check_duplicate_file(file_save_path):
        print("There is a file with the same name in that path")
        update_progress(status="warning")
        if QMessageBox.warning(None, program_title_local, f"{file_save_path}\n\nThere is a file with a duplicate name in the path.\nDo you want to overwrite?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            file_save_path = get_non_duplicate_filename(file_save_path)
            if QMessageBox.warning(None, program_title_local, f"{file_save_path}\n\nWould you like to save it with the name above?\nIf you select No, all progress will be cancelled.", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return 1
    
    print(f"File name check completed")
    update_progress(95)

    # File Save
    print("File Saving...")
    try:
        with open(file_save_path, "wb") as file_write_data:
            file_write_data.write(deced_org_file_data)
    except Exception as e:
        print(f"An error occurred while saving: {e}")
        print(f"Please try again from the beginning.")
        update_progress(status="error")
        return 2
    print(f"File Saved: [{file_save_path}]")
    update_progress(100)
    
    # org File delete
    ### I don’t think so..
    # print("deleting org file...")
    # delete_file(org_file_path)

    # task complit
    print("File encryption success")
    return [0, file_save_path]

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
            return None
        
        return file_path

def files_select():
    global program_title
    program_title_local = (program_title + " - Files select")

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

def get_non_duplicate_filename(file_path):
    file_dir = remove_filename_from_path(file_path)
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    new_file_path = file_path
    counter = 0

    while os.path.exists(new_file_path):
        counter += 1
        new_file_name = f"{file_name} ({counter}){file_extension}"
        new_file_path = os.path.join(file_dir, new_file_name)

    return new_file_path

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
    global file_identifier
    try:
        with open(file_path, 'rb') as file_data:
            data = file_data.read()

            # base64 decode
            print("base64 decoding...")
            data = base64.b64decode(data)
            print("base64 decoded")
            
            print("Finding identifier...")
            index = data.find(file_identifier)
            if index != -1:
                data_after_sign = data[:index]
                data_before_sign = data[index + len(file_identifier):]
                print("Identifier Finded")
                return (data_after_sign, data_before_sign)
            else:
                print("The identifier was not found in the file data.")
                return 4

    except Exception as e:
        print(f"An error occurred: {e}")
        return 2

def check_valid_password(input_string):
    min_len = 1
    max_len = 65536
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