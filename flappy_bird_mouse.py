import sys
import time
import pyautogui
import threading
import tkinter as tk
import keyboard
import random
import sys

gameloop = True
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1 / 60   
# SCOOOREBOOOARD SCOORBOARD
scoretk = tk.Tk()
scoretk.title("Mouse Flappy Bird Score")
scoretk.geometry("200x100+20+20")
scoretk.resizable(False, False)
scoretk.overrideredirect(True)
scoretk.attributes("-topmost", True)
scoretk.configure(bg="#2c2c2c")
score_var = tk.IntVar(value=0)
score_label = tk.Label(scoretk, textvariable=score_var, font=("Helvetica", 40, "bold"), fg="white", bg="#2c2c2c")
score_label.pack(expand=True)
#pip ees
top = tk.Toplevel(scoretk)
top.resizable(False, False)
top.title("Top Pipe")
top.configure(bg="#337c08")
top.geometry("100x250+800+0")
#bootom pipe
bottom = tk.Toplevel(scoretk)
bottom.resizable(False, False)
bottom.title("Bottom Pipe")
bottom.configure(bg="#337c08")
bottom.geometry(f"100x{bottom.winfo_screenheight() - 250}+800+{str(bottom.winfo_screenheight() - 250)}")

def fullscreenbg():
     bg = tk.Toplevel(scoretk)
     bg.attributes("-fullscreen", True)
     bg.config(bg="#008ACA")


def restart_game(lose_window):
    global score_var
    score_var.set(0)
    global gameloop
    gameloop = True
    scoretk.deiconify()
    top.deiconify()
    bottom.deiconify()
    lose_window.destroy()
    
def Losemenu():
    pyautogui.moveTo(scoretk.winfo_screenwidth() // 2, scoretk.winfo_screenheight() // 2)
    lose_window = tk.Toplevel(scoretk)
    lose_window.protocol("WM_DELETE_WINDOW", scoretk.destroy)
    global score_var 
    scoretk.withdraw()
    top.iconify()
    bottom.iconify()
    lose_window.title("You Lose!")
    lose_window.geometry(f"300x200+{(lose_window.winfo_screenwidth() // 2) - 150 }+{(lose_window.winfo_screenheight() // 2) - 100}")
    lose_window.resizable(False, False)
    lose_window.configure(bg="#2c2c2c")
    lose_label = tk.Label(lose_window, text="You Lose! \n (close the x to exit)", font=("Helvetica", 20, "bold"), fg="white", bg="#2c2c2c")
    lose_label.pack(pady=20)
    score_label = tk.Label(lose_window, text=f"Score: {score_var.get()}", font=("Helvetica", 16), fg="white", bg="#2c2c2c")
    score_label.pack()
    restart_button = tk.Button(lose_window, text="Restart", font=("Helvetica", 14), command=lambda: restart_game(lose_window))
    restart_button.pack(pady=1)

def mouseflap():
    global gameloop
    GRAV = 0
    last_frame_jumped = False
    while True:
            if gameloop:
                    space_down = keyboard.is_pressed("space")

                    if space_down and not last_frame_jumped:
                        GRAV = -10          
                    GRAV += 0.5
                    pyautogui.moveRel(0, GRAV)

                    last_frame_jumped = space_down
                    GRAV += 0.5
                    pyautogui.moveRel(0, GRAV)
                    
            else:
                 GRAV = 0
                 last_frame_jumped
                 time.sleep(0.1)

def pipes():
    global gameloop
    while True:
        if gameloop:
            gap = scoretk.winfo_screenheight() // 5
            pipes_x = bottom.winfo_screenwidth() + 100
            top_y = 0
            top_height = random.randint(50, 400)
            bottom_y = top_height + gap
            bottom_height = bottom.winfo_screenheight() - bottom_y
            while pipes_x > -105:
                pipes_x -= 5
                top.geometry(f"100x{top_height}+{pipes_x}+{top_y}")
                bottom.geometry(f"100x{bottom_height}+{pipes_x}+{bottom_y}")
                mousex, mousey = pyautogui.position()
                if mousey <= 15 or mousey >= bottom.winfo_screenheight() - 15:
                        gameloop = False
                        Losemenu()
                        break
                if (pipes_x < mousex < pipes_x + 100) and (mousey < top_height or mousey > bottom_y):
                    gameloop = False
                    Losemenu()
                    break
                time.sleep(0.01)
            score_var.set(score_var.get() + 1)
        else:
            time.sleep(0.1)



flap_thread = threading.Thread(target=mouseflap, daemon=True)
pipe_thread = threading.Thread(target=pipes, daemon=True)
if __name__ == "__main__":
    try:
        if not "-desktop" in sys.argv:
            fullscreenbg()
        flap_thread.start()
        pipe_thread.start()
        scoretk.mainloop()
    except KeyboardInterrupt:
        print("Fail-safe triggered!! no more mouse flappy bird until you boot me up again")