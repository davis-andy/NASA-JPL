from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from subprocess import Popen
from main import main_program
from backend.globals.instruments import set_instrs
from backend.globals.settings import VERSIONS_FILE_PATH, SOFTWARE_VERSION, METSRV_PATH, INSTALLER_LAUNCHER
from backend.daq.settings import SOFTWARE_VERSION as DAQ_VERSION

# Initialize a window
window = Tk()

# Determine window size
windowWidth = 545
windowHeight = 385

# Get monitor size
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

# Center point for window
centerX = int((screenWidth/2) - (windowWidth/2))
centerY = int((screenHeight/2) - (windowHeight/2))

# Window attributes
window.resizable(width=False, height=False)
window.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
window.config(bg='#FFF')
# Hide the title bar
window.overrideredirect(True)

# Insert logo
img = Image.open('frontend/images/globals/logo_icon.png').resize((windowWidth // 2, windowHeight // 2), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(img)
bg_label = Label(window, image=bg, bg='#FFF')
bg_label.pack(pady=50)

# Label Text of what is going on
load_text = StringVar()
load_text.set('Checking for Updates...')
load = Label(window, textvariable=load_text, fg='#5D5D60', bg='#FFF', font=('Arial', 25))
load.pack()


# Destroy the application
def goodbye():
    window.destroy()


# Check the versions file for updates
def update_check():
    version_dict = {}
    title = 'Update Software?'
    msg = 'Do you wish to update your software at this time?'
    update = False
    try:
        version_file = open(VERSIONS_FILE_PATH)
    except:
        load_text.set('Updates failed...')
        window.after(500, instrument_check)
        return
    with version_file:
        for line in version_file:
            line = line.rstrip()
            temp_line = line.split(',')
            version_dict[temp_line[0]] = temp_line[1]

    for prog, vers in version_dict.items():
        if prog.lower() == 'suite' and vers > SOFTWARE_VERSION:
            update = True
            break
        elif prog.lower() == 'daqcards' and vers > DAQ_VERSION:
            update = True
            break
        else:
            continue

    # Ask user if they want to update their program
    if update:
        mb = messagebox.askyesno(title, msg)
        if not mb:
            load_text.set('Searching for instruments...')
            window.after(100, instrument_check)
        else:
            Popen(['powershell.exe', rf'{METSRV_PATH}{INSTALLER_LAUNCHER}'])
            window.after(100, goodbye)
    else:
        load_text.set('Searching for instruments...')
        window.after(100, instrument_check)


# Check for connected instruments
def instrument_check():
    set_instrs()
    load_text.set('Loading Main Program...')
    load_main()


# Run the main program
def load_main():
    window.after(500, main_program)


window.after(500, update_check)
