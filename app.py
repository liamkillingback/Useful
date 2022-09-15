import tkinter as tk
from tkinter import W, Entry, Toplevel, filedialog, Text
import os
import webbrowser
import re
from googleapiclient.discovery import build

# Create and initialize the body, lists and title.
root = tk.Tk()
apps = []
appNames = []
root.title("Super file launcher 9000")

# Checks if there is already saved programs/Url's
if os.path.isfile('save.txt'):
    with open('save.txt', 'r',) as f:
        tempApps = f.read()
        tempApps = tempApps.split(',')
        apps = [x for x in tempApps if x.strip()]
# Same as above but for simplified names
if os.path.isfile('names.txt'):
    with open('names.txt', 'r', encoding="utf-8") as file:
        tempApps2 = file.read()
        tempApps2 = tempApps2.split(',')
        appNames = [x for x in tempApps2 if x.strip()]

# Prompts for a file directory and saves it in the .txt files
def addApp():
    for widget in frame.winfo_children():
        widget.destroy()
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", 
    filetypes=(("executables", "*.exe"), ("all files", "*.*")))
    apps.append(filename)
    # This part gives us a simplified name of the file, rather than the directory
    name = re.findall('(?:.(?!/))+$', filename)
    temp = name[0]
    temp = temp.replace("/", "")
    temp = temp.replace(".exe", "")
    appNames.append(temp)
    # Adds the filenames (appNames) to the list on the program window
    for app in appNames:
        label = tk.Label(frame, text=app, bg="#85C1E9", font="Helvetica 12 bold")
        label.pack()
    
# Runs file if it starts with C (Verifies its a local directory), or launches a browser if filename contains .com
def runApps():
    subString = '.com'
    for app in apps:
        if app[0] == 'C':
            os.startfile(app)
        if subString in app:
            webbrowser.open(app)

# Clears all saved files/Url's to reconfigure setup
def clearCache():
    if os.path.exists('save.txt'):
        apps.clear()
        os.remove('save.txt')
    if os.path.exists('names.txt'):
        appNames.clear()
        os.remove('names.txt')
    else:
        print('The file does not exist')
    tk.messagebox.showinfo('Cache deleted', 'Cache deleted')

# popup window appears and prompts user to enter a web address
def WebPopUp():
    def addURL():
        # If the url is a youtube video, it will parse the video name into the widget, rather than the url
        if "youtube" in entry.get():
            video_id = entry.get()[len("https://www.youtube.com/watch?v="):]
        else:
            video_id = entry.get()
  
        # creating youtube resource object 
        youtube = build('youtube','v3',developerKey='AIzaSyBygHcjC8Lz9XOL8DoB3Ivc8mySSYRna4g')
  
        # retrieve youtube video results
        video_request=youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        )
  
        video_response = video_request.execute()
    
        title = video_response['items'][0]['snippet']['title']
        # Verifies user submittion, then closes the popup window
        tk.messagebox.showinfo('Submitted!', 'Submitted')
        apps.append(video_id)
        appNames.append(title)
        top.destroy()

    top = Toplevel(root)
    top.geometry("500x200")
    header2 = tk.Label(top, text="Enter URL", fg="black", bg="#85C1E9", font="Helvetica 16 bold italic")
    header2.pack()
    entry = Entry(top, width=100)
    entry.pack()
    subBut = tk.Button(top, text="Submit", padx=10, pady=5, fg="white", bg="#263D42", command=addURL)
    subBut.pack()

# Creates the body
canvas = tk.Canvas(root, height=550, width=700, bg="#2980B9")
canvas.pack()
# Creates a frame around the body
frame = tk.Frame(root, bg="#85C1E9")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
# Button for opening a file directory
openFile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#263D42", command=addApp)
openFile.place(x=100, y=450)
# Button to run apps
runApps = tk.Button(root, text="Run Apps", padx=10, pady=5, fg="white", bg="#263D42", command=runApps)
runApps.place(x=225, y=450)
# clear cache button
clear = tk.Button(root, text="Clear Cache", padx=10, pady=5, fg="white", bg="#263D42", command=clearCache)
clear.place(x=360, y=450)
# header 
header = tk.Label(root, text="Startup List: ", fg="black", bg="#85C1E9", font="Helvetica 16 bold italic")
header.place(x=70, y=15)
# button for url additions
webBut = tk.Button(root, text="Add web URL", padx=10, pady=5, fg="white", bg="#263D42", command=WebPopUp)
webBut.place(x=500, y=450)
# Makes the window non-resizable
root.resizable(False, False)

# Adds appnames/Urls to the main window
for app in appNames:
    label = tk.Label(frame, text=app, bg="#85C1E9", font="Helvetica 12 bold")
    label.pack()

root.mainloop()

# Creates or opens a .txt to store user preset
with open('save.txt', 'w') as f:
    for app in apps:
        f.write(app + ',')
# As above but for file names, not addresses
with open('names.txt', 'w', encoding="utf-8") as file:
    for app in appNames:
        file.write(app + ',')
