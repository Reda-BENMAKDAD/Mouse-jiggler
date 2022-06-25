import tkinter
import pyautogui
import multiprocessing
from time import sleep
from random import randint
from functools import partial

root = tkinter.Tk() # the main window is created outside the main function for reachability reasons

monitor_width = pyautogui.size()[0]
monitor_height = pyautogui.size()[1]

# this creats a notification window 
# and displays the message given as parameter
def info(message):
    info_window = tkinter.Tk()
    info_window.title("Info")
    info_window.iconbitmap("./assets/mouse-icon.ico")
    info_window.geometry("300x200")
    info_label = tkinter.Label(info_window, text=message)
    info_label.place(x=50, y=50)
    info_window.mainloop()


# the function that jiggles the mouse
def jiggle() -> None:
    while True:
        x = randint(0, monitor_width)
        y = randint(0, monitor_height)
        pyautogui.moveTo(x, y, 0.25)
        sleep(5)
        pyautogui.press('shift')

        sleep(5)       
        pyautogui.press('b')
        sleep(5)
        pyautogui.press('backspace')

# since the jiggler function is blocking
# it is ran in a different process to avoid blocking the main thread
process = multiprocessing.Process(target=jiggle)



# called on click of the start button and starts the jiggle process
def startproc(status_circle: tkinter.Canvas) -> None:
    global root
    global process
    if process.is_alive():
        info("mouse jiggler already running")
        return;
    else:
        # process variable is redefined since you can't restart a terminated process
        process = multiprocessing.Process(target=jiggle)
        process.start()
        # this changes the color of the little square to green
        # to indicate that the process is running
        status_circle.configure(bg="#00ff34")
        status_circle.update()
        root.update()

# called on click of the stop button
def stopproc(status_circle) -> None:
    global root
    global process
    if not process.is_alive():
        info("mouse jiggler is not running")
        return;
    else :
        process.terminate()
        # this changes the color of the little square to gray
        # to indicate that the process is stopped
        status_circle.configure(bg="#6b706c")
        status_circle.update()
        root.update()
 
# this function is called when the window is closed from the X button
# it stops the jiggle process and closes the window
def safe_close() -> None :
    global root
    global process
    if process.is_alive():
        process.terminate()  

    root.destroy(); 

# main function that runs the main window
def main():
    global root
    root.title("Mouse jiggler")
    root.iconbitmap("./assets/mouse-icon.ico")
    root.configure(background="#7f7dfa")
    root.geometry("310x150")
    status_circle = tkinter.Canvas(root, width=10, height=10, bg="#6b706c", borderwidth=0, highlightthickness=0)
    status_circle.place(x=280, y=15)
    btn_giggle = tkinter.Button(root, text="start", command=partial(startproc, status_circle))
    btn_giggle.place(x=70, y=70)
    btn_stop = tkinter.Button(root, text="stop", command=partial(stopproc, status_circle))
    btn_stop.place(x=190, y=70)
    root.protocol("WM_DELETE_WINDOW", safe_close)

    root.mainloop()

if __name__ == '__main__':
    main()