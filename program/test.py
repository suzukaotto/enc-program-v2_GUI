from tkinter import TOP, Label, StringVar
from tkinterdnd2 import *

def get_path(event):
    pathLabel.configure(text=event.data)

root = TkinterDnD.Tk()
root.geometry("350x100")
root.title("Get file path")

pathVar = StringVar()

pathLabel = Label(root, text="Drag and drop file here")
pathLabel.pack(side=TOP, padx=5, pady=5)

pathLabel.drop_target_register(DND_ALL)
pathLabel.dnd_bind("<<Drop>>", get_path)

root.mainloop()
