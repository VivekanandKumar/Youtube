from threading import Thread
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import ctypes
from pytube import *
import os
import requests
from PIL import Image, ImageTk


def passcurrentstrm(f):
    global currentStream
    currentStream = f


def download():
    download = Thread(target=downloadVideo)
    download.start()


def downloadVideo():
    try:
        t = path_input.cget("text")
        if t == "":
            messagebox.showwarning(
                "Warning", "Please provide destination path")
            return

        if chooser.current() > 0:
            messagebox.showinfo(
                "Information", "Your downloading is started......")
            currentStream.download(t)
            messagebox.showinfo(
                "Information", "Download Completed")
        else:
            messagebox.showwarning(
                "Warning", "Please Choose a video resolution...")
            return

    except Exception as e:
        print("Error in Downloading ", e)


def selectedResolution(event):
    item = selectedItem.get()

    def getItem():
        try:
            currentstrm = strm.get_by_itag(resDict.get(item))
            passcurrentstrm(currentstrm)
            size = sizeinmb(currentstrm.filesize)
            fileSize.config(text=size)
        except Exception as e:
            print(e)

    def getResSize():
        t3 = Thread(target=getItem)
        t3.start()
    getResSize()


def getPath():
    t1 = Thread(target=pathdir)
    t1.start()


def pathdir():
    try:
        path = filedialog.askdirectory()
        path_input.config(text=path)

    except Exception as e:
        print(e)


def getResList(dict):
    return list(dict.keys())


def getInfo():
    t2 = Thread(target=mediaInfo)
    t2.start()


def sizeinmb(byte):
    mb = byte/(1024*1024)
    return "{:00.0f} MB".format(mb)


def isUrlValid(url):
    try:
        pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
        request = requests.get(url)
        return False if pattern in request.text else True
    except Exception as e:
        #  print(e)
        return


resDict = {}


def mediaInfo():
    try:
        fileSize.config(text="")
        resDict.clear()
        url = url_input.get()
        if(not isUrlValid(url)):
            messagebox.showwarning("Warning", "Invalid URL.....")

            return
        video = YouTube(url)
        global strm
        strm = video.streams.filter(
            progressive=True).order_by('resolution').desc()

        video_title = video.title
        thumb_url = video.thumbnail_url
        duration = changeTime(video.length)

        image = Image.open(requests.get(thumb_url, stream=True).raw)
        img = image.resize((300, 225), None)
        global myImg
        myImg = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=NW, image=myImg)

        for item in strm:
            resDict.update({item.resolution: item.itag})

        title.config(text=video_title)

        videoLength.config(text=duration)
        chooser.config(value=["Choose Resolution...."] + getResList(resDict))
        chooser.current(0)
    except Exception as e:
        print("Error in getting data : ", e)


def changeTime(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%2d Hr %2d Min %2d Sec" % (hour, minutes, seconds)


app = Tk()
style = ttk.Style()
app.tk.call("source", "Azure/azure.tcl")
app.tk.call("set_theme", "dark")
current_theme = style.theme_use()

userPc = ctypes.windll.user32
mainWidth = userPc.GetSystemMetrics(0)
mainHeight = userPc.GetSystemMetrics(1)
window_width = 650
centerX = int((mainWidth / 2) - (window_width / 2))

app.geometry(f'{window_width}x{600}+{centerX}+{15}')
app.config(
    bg="#333"
)
app.minsize(700, mainHeight-100)
app.title("YouTube Video Downloader")
app.iconbitmap('images/logo.ico')

root = Frame(app, bg="#474747")

root.pack(ipady=mainHeight)

topFrame = Frame(
    root,
    background="#1e1f26",
)
topFrame.grid(row=0, column=0, sticky=W, ipadx=84)

img = PhotoImage(file='images/logo.png')
logo = Label(
    topFrame,
    image=img,
    background="#1e1f26"
).grid(row=0, column=0, ipadx=10)

header = Label(
    topFrame,
    text="YOUTUBE VIDEO DOWNLOADER",
    foreground="#fafafa",
    font=("Segoe UI Semilight", 20),
    background="#1e1f26"
).grid(row=0, column=1, ipadx=10)

inputFrame = Frame(
    root,
    background="#474747"
)
inputFrame.grid(sticky=W, row=1, column=0)
style.configure(
    'TLabel',
    foreground="#FAFAFA",
    background="#474747"
)
canvas = Canvas(
    inputFrame,
    bg="#5a5a5a",
    width=300,
    height=225,
    bd=0,
    highlightthickness=0
)
canvas.grid(row=0, column=2, rowspan=5, pady=10, padx=10)


url_label = ttk.Label(
    inputFrame,
    text="Enter Video URL",
    font=('Segoe UI Semilight', 14),
    style='TLabel',
).grid(sticky=W, row=0, column=0, padx=10, pady=10)

url_input = Entry(
    inputFrame,
    width=30,
    background="#5a5a5a",
    foreground='#fafafa',
    font=('Segoe UI Light', 14),
    relief=FLAT,
    insertbackground='#fafafa',
    bd=6
)
url_input.grid(sticky=W, row=1, column=0, padx=10)
go_img = PhotoImage(file='images/go.png')
goBtn = Button(
    inputFrame,
    cursor='hand2',
    image=go_img,
    bg="#474747",
    relief=FLAT,
    activebackground='#474747',
    bd=0,
    command=getInfo
)
goBtn.grid(row=1, column=1)

path_label = ttk.Label(
    inputFrame,
    text="Choose Destination Path",
    font=('Segoe UI Semilight', 14),
    style='TLabel',
).grid(sticky=W, row=2, column=0, padx=10, pady=5)
style.map("TEntry", fieldbackground=[("active", "black"), ("disabled", "red")])

path_input = Label(
    inputFrame,
    width=30,
    text=os.getcwd(),
    background="#5a5a5a",
    foreground="white",
    font=('Segoe UI Light', 14),
    relief=FLAT,
    anchor=W,
    bd=6
)
path_input.grid(sticky=W, row=3, column=0, padx=10)
folder_img = PhotoImage(file='images/folder.png')
folder_label = Button(
    inputFrame,
    cursor='hand2',
    image=folder_img,
    bg="#474747",
    relief=FLAT,
    activebackground='#474747',
    bd=0,
    command=getPath
)
folder_label.grid(row=3, column=1)
bigfont = ('Segoe UI Light', 14)

app.option_add("*TCombobox*Listbox*Font", bigfont)
selectedItem = StringVar()
chooser = ttk.Combobox(
    inputFrame,
    width=35,
    cursor='hand2',
    font=('Segoe UI Light', 14),
    state='readonly',
    textvariable=selectedItem
)
chooser.bind('<<ComboboxSelected>>', selectedResolution)
chooser.grid(sticky=W, row=4, column=0, columnspan=2, padx=10, pady=10)
style.configure(
    'ttk.TLabel',
    foreground="#FAFAFA",
    background="#5a5a5a"
)
title_label = ttk.Label(
    inputFrame,
    text="Title",
    font=('Segoe UI Semilight', 14),
    style='TLabel',
).grid(sticky=W, row=5, column=0, padx=10, pady=10)

title = ttk.Label(
    inputFrame,
    width=67,
    font=('Segoe UI Semilight', 14),
    style='ttk.TLabel',
)
title.grid(sticky=W, row=6, column=0, padx=10, columnspan=3, ipady=5, ipadx=5)

size_label = ttk.Label(
    inputFrame,
    text="File Size",
    font=('Segoe UI Semilight', 14),
    style='TLabel',
).grid(sticky=W, row=7, column=0, padx=10, pady=10)

fileSize = ttk.Label(
    inputFrame,
    width=30,
    font=('Segoe UI Semilight', 14),
    style='ttk.TLabel'
)
fileSize.grid(sticky=W, row=8, column=0, padx=10, ipadx=5, ipady=5)

length_label = ttk.Label(
    inputFrame,
    text="Video Length",
    font=('Segoe UI Semilight', 14),
    style='TLabel',
).grid(sticky=W, row=7, column=1, columnspan=2, padx=29, pady=10)

videoLength = ttk.Label(
    inputFrame,
    width=30,
    font=('Segoe UI Semilight', 14),
    style='ttk.TLabel'
)
videoLength.grid(sticky=W, row=8, column=1,
                 columnspan=2, padx=29, ipadx=5, ipady=5)

style.map("C.TButton",
          foreground=[('!active', 'black'),
                      ('pressed', 'red'), ('active', 'white')],
          background=[('!active', 'grey75'),
                      ('pressed', 'green'), ('active', 'black')]
          )
downloadBtn = Button(
    inputFrame,
    width=68,
    text="Download",
    relief=FLAT,
    bg="#ffdf8f",
    fg="#333",
    font=('Segoe UI Semilight', 14),
    activebackground='#1e1f26',
    bd=0,
    cursor='hand2',
    command=download
).grid(row=9, column=0, columnspan=3, sticky=W, padx=10, pady=30, ipady=5)

app.mainloop()
