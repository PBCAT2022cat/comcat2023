from tkinter import Text, font as f
from tkinter import *
from tkinter.messagebox import *#弹窗库
from tkinter.filedialog import *
import sys,os
import hashlib


if len(sys.argv)>1:
    file = sys.argv[1]

file = None

def opens(event=None):
    global file
    text.delete(1.0,"end")
    file = askopenfilename()
    if file:
        with open(file,'r') as f:
            text.insert('insert',f.read())
        win.title(file+'-Comcat Writer')
def newFile():
    global file
    text.delete(1.0,"end")
    file = None
    win.title(str(file)+'-Comcat Writer')
def delFile():
    file = askopenfilenames()
    if file:
        if askokcancel("system","delet this files true?"):
            for i in file:
                os.remove(i)
def save(event=None):
    global file
    if file == None:
        file = asksaveasfilename()
    if file:
        with open(file,'w') as f:
            f.write(getSig())
def getWin():
    global w,h
    if w != win.winfo_width() and h != win.winfo_height():
        w,h = win.winfo_width(),win.winfo_height()
        text.config(width=win.winfo_width(),height=win.winfo_height())
    win.after(1,getWin)

def move():
    text.edit_undo()
def getSig():
    contents = text.get(1.0, "end")
    return contents
def callback(event):
    text.edit_separator()

win = Tk()
win.geometry("1000x800")
win.title(str(file)+'-Comcat Writer')
w,h = win.winfo_width(),win.winfo_height()

text = Text(win,autoseparators=False, undo=True, maxundo=10)
text.bind('<Key>', callback)
text.bind_all('<Control-s>',save)
text.bind_all('<Control-o>',opens)
#MENU
menu_all = Menu(win)
file_menu = Menu(menu_all,tearoff=0)
run_menu = Menu(menu_all,tearoff=0)
edit_menu = Menu(menu_all,tearoff=0)

open_bt = Menu(file_menu,tearoff=0)
new_bt = Menu(file_menu,tearoff=0)
save_bt = Menu(file_menu,tearoff=0)

file_menu.add_command(label='save',command=save)
file_menu.add_command(label='open',command=opens)
file_menu.add_command(label='new',command=newFile)
file_menu.add_command(label='delet',command=delFile)


back_bt = Menu(edit_menu,tearoff=0)
edit_menu.add_command(label='back',command=move)

menu_all.add_cascade(label='File',menu=file_menu)
menu_all.add_cascade(label='Edit',menu=edit_menu)
menu_all.add_cascade(label='Run',menu=run_menu)
#MENU END

win.config(menu=menu_all)
text.pack()

getWin()

win.mainloop()
