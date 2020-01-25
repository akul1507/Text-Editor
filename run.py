from tkinter import *
import os
from tkinter import simpledialog
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad:
    # variables
    root = Tk()

    # default window width and height
    thisWidth = 300
    thisHeight = 300
    thisTextArea = Text(root, undo=True)
    thisMenuBar = Menu(root)
    thisFileMenu = Menu(thisMenuBar, tearoff=0)
    thisEditMenu = Menu(thisMenuBar, tearoff=0)
    thisHelpMenu = Menu(thisMenuBar, tearoff=0)
    thisFindMenu = Menu(thisMenuBar, tearoff=0)
    thisScrollBar = Scrollbar(thisTextArea)
    file = None

    def __init__(self, **kwargs):
        # initialization

        # set icon
        try:
            self.root.wm_iconbitmap("Notepad.ico")  # GOT TO FIX THIS ERROR (ICON)
        except:
            pass

        # set window size (the default is 300x300)

        try:
            self.thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.thisHeight = kwargs['height']
        except KeyError:
            pass

        # set the window text
        self.root.title("Untitled - Text Editor")

        # center the window
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        left = (screenWidth / 2) - (self.thisWidth / 2)
        top = (screenHeight / 2) - (self.thisHeight / 2)

        self.root.geometry('%dx%d+%d+%d' % (self.thisWidth, self.thisHeight, left, top))

        # to make the textarea auto resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # add controls (widget)

        self.thisTextArea.grid(sticky=N + E + S + W)

        self.thisFileMenu.add_command(label="New", command=self.newFile, accelerator='Ctrl+N')
        self.thisFileMenu.add_command(label="Open", command=self.openFile, accelerator='Ctrl+O')
        self.thisFileMenu.add_command(label="Save", command=self.saveFile, accelerator='Ctrl+S')
        self.thisFileMenu.add_separator()
        self.thisFileMenu.add_command(label="Exit", command=self.quitApplication, accelerator='Ctrl+Q')
        self.thisMenuBar.add_cascade(label="File", menu=self.thisFileMenu)

        self.thisEditMenu.add_command(label="Select All", command=self.select_all, accelerator='Ctrl+A')
        self.thisEditMenu.add_separator()
        self.thisEditMenu.add_command(label="Undo", command=self.undo, accelerator='Ctrl+Z')
        self.thisEditMenu.add_command(label="Redo", command=self.redo, accelerator='Ctrl+Y')
        self.thisEditMenu.add_separator()
        self.thisEditMenu.add_command(label="Cut", command=self.cut, accelerator='Ctrl+X')
        self.thisEditMenu.add_command(label="Copy", command=self.copy, accelerator='Ctrl+C')
        self.thisEditMenu.add_command(label="Paste", command=self.paste, accelerator='Ctrl+V')
        self.thisMenuBar.add_cascade(label="Edit", menu=self.thisEditMenu)

        self.thisFindMenu.add_command(label="Find", command=self.find, accelerator='Ctrl+F')
        self.thisFindMenu.add_command(label="Replace", command=self.replace, accelerator='Ctrl+H')
        self.thisMenuBar.add_cascade(label="Find", menu=self.thisFindMenu)

        self.thisHelpMenu.add_command(label="About Notepad", command=self.showAbout, accelerator='F1')
        self.thisMenuBar.add_cascade(label="Help", menu=self.thisHelpMenu)

        self.root.config(menu=self.thisMenuBar)

        self.thisScrollBar.pack(side=RIGHT, fill=Y)
        self.thisScrollBar.config(command=self.thisTextArea.yview)
        self.thisTextArea.config(yscrollcommand=self.thisScrollBar.set)

        self.thisTextArea.bind("<Control-Key-n>", self.newFile)
        self.thisTextArea.bind("<Control-Key-o>", self.openFile)
        self.thisTextArea.bind("<Control-Key-s>", self.saveFile)
        self.thisTextArea.bind("<Control-Key-q>", self.quitApplication)
        self.thisTextArea.bind("<Control-Key-a>", self.select_all)
        self.thisTextArea.bind("<Control-Key-z>", self.undo)
        self.thisTextArea.bind("<Control-Key-y>", self.redo)
        self.thisTextArea.bind("<Control-Key-f>", self.find)
        self.thisTextArea.bind("<Control-Key-h>", self.replace)
        self.thisTextArea.bind("<F1>", self.showAbout)

    def quitApplication(self, event=None):
        self.root.destroy()
        # exit()

    def showAbout(self, event=None):
        showinfo("Text Editor", "Created by: Akul Gupta")

    def openFile(self, event=None):
        fileOpen = askyesnocancel("New File", "Do you want to save this file before opening a new file?")

        if fileOpen is True:
            self.saveFile()

        elif fileOpen is None:
            return

        self.file = askopenfilename(defaultextension=".txt",
                                    filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

        if self.file:
            self.root.title(os.path.basename(self.file) + " - Text Editor")
            self.thisTextArea.delete(1.0, END)
            with open(self.file, 'r') as file:
                self.thisTextArea.insert(1.0, file.read())

    def newFile(self, event=None):
        createFile = askyesnocancel("New File", "Do you want to save this file before creating a new file?")
        if createFile is True:
            self.saveFile()
        elif createFile is None:
        	return
        
        self.root.title("Untitled - Text Editor")
        self.file = None
        self.thisTextArea.delete(1.0, END)

    def saveFile(self, event=None):

        if not self.file:
            self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

        if self.file:
            with open(self.file, 'w') as file:
                file.write(self.thisTextArea.get(1.0, END))
            self.root.title(os.path.basename(self.file) + " - Text Editor")

    def select_all(self, event=None):
        self.thisTextArea.tag_add('sel', '1.0', 'end')
        return 'break'

    def find(self, event=None):
        try:
            self.thisTextArea.tag_remove('highlight', '1.0', END)
        except:
            pass

        string = simpledialog.askstring("Find String", "")

        if string == '' or string is None:
            return

        start_pos = self.thisTextArea.search(string, '1.0', stopindex=END)
        # print('{!r}'.format(start_pos))
        while start_pos:
            end_pos = '{}+{}c'.format(start_pos, len(string))
            # print('{!r}'.format(end_pos))
            self.thisTextArea.tag_add('highlight', start_pos, end_pos)
            self.thisTextArea.tag_config('highlight', foreground='red')
            start_pos = self.thisTextArea.search(string, end_pos, stopindex=END)

    def replace(self, event=None):

        string = simpledialog.askstring("Find String", "")

        if string is not None:
            string2 = simpledialog.askstring("Replacement String", "")

        if string is None or string == '':
            return

        temp = self.thisTextArea.get('1.0', END).replace(string, string2)
        self.thisTextArea.delete('1.0', END)
        self.thisTextArea.insert('1.0', temp)

    def undo(self, event=None):
        try:
            self.thisTextArea.edit_undo()
        except:
            pass

    def redo(self, event=None):
        try:
            self.thisTextArea.edit_redo()
        except:
            pass

    def cut(self):
        self.thisTextArea.event_generate("<<Cut>>")

    def copy(self):
        self.thisTextArea.event_generate("<<Copy>>")

    def paste(self):
        self.thisTextArea.event_generate("<<Paste>>")

    def run(self):

        # run main application

        self.root.mainloop()


# run main application
notepad = Notepad(width=800, height=800)
notepad.run()
