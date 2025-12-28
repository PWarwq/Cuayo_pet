import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import time
import os
import random
import platform

# OS Detect
OS_TYPE = platform.system()
if OS_TYPE == "Windows":
    import pygetwindow as gw
else:
    try:
        from Xlib import display, X
    except ImportError:
        print("Linux detected: Please run 'pip install python-xlib' for window detection features.")

class SingleCuayo:
    def __init__(self, parent_win, assets, size):
        self.pet_win = tk.Toplevel(parent_win)
        self.pet_win.overrideredirect(True)
        self.pet_win.attributes('-topmost', True)
        
        if OS_TYPE == "Windows":
            self.pet_win.wm_attributes('-transparentcolor', 'black')
        
        self.assets = assets
        self.size = size
        self.x = random.randint(100, 800)
        self.y = random.randint(100, 500)
        self.vel_x = random.choice([-5, 5])
        self.vel_y = random.choice([-5, 5])
        
        self.state = "MOVE"
        self.state_timer = time.time()
        self.coayo_timer = time.time()
        self.bounce_visual_timer = 0
        
        self.label = tk.Label(self.pet_win, image=self.assets['normal_r'], bg='black', bd=0)
        self.label.pack()
        
        self.pet_win.bind("<Button-3>", lambda e: self.remove())

    def update(self, is_muted, speed_mult):
        if not self.pet_win.winfo_exists(): return
        
        screen_w = self.pet_win.winfo_screenwidth()
        screen_h = self.pet_win.winfo_screenheight()
        now = time.time()

        if now - self.state_timer > random.uniform(2, 6):
            self.state = random.choice(["MOVE", "MOVE", "IDLE"])
            if self.state == "MOVE":
                self.vel_x = random.choice([-5, -3, 3, 5]) * speed_mult
                self.vel_y = random.choice([-5, -3, 3, 5]) * speed_mult
            self.state_timer = now

        if self.state == "MOVE":
            self.x += self.vel_x
            self.y += self.vel_y

        hit = False
        if self.x <= 0: self.x = 5; self.vel_x = abs(self.vel_x); hit = True
        elif self.x >= screen_w - self.size: self.x = screen_w - self.size - 5; self.vel_x = -abs(self.vel_x); hit = True
        if self.y <= 0: self.y = 5; self.vel_y = abs(self.vel_y); hit = True
        elif self.y >= screen_h - self.size: self.y = screen_h - self.size - 5; self.vel_y = -abs(self.vel_y); hit = True

        if hit:
            if not is_muted: self.assets['s_bounce'].play()
            self.bounce_visual_timer = now + 0.4
            self.coayo_timer = now

        img = self.assets['normal_r']
        if now < self.bounce_visual_timer:
            img = self.assets['bounce_l'] if self.vel_x < 0 else self.assets['bounce_r']
        else:
            img = self.assets['normal_l'] if self.vel_x < 0 else self.assets['normal_r']
        self.label.config(image=img)

        if now - self.coayo_timer >= 2.0:
            if self.state != "IDLE" and not is_muted: self.assets['s_coayo'].play()
            self.coayo_timer = now

        self.pet_win.geometry(f"{self.size}x{self.size}+{int(self.x)}+{int(self.y)}")

    def trigger_rotate(self, is_muted):
        if not is_muted: self.assets['s_rotate'].play()
        self.state = "MOVE"
        self.vel_x *= 1.2

    def remove(self):
        self.pet_win.destroy()

class CuayoManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Cuayo Control")
        self.root.geometry("300x450")
        self.root.configure(bg='#1e1e2e')
        
        pygame.mixer.init()
        self.size = 100
        self.pets = []
        self.is_muted = False
        self.speed_mult = 1.0
        self.last_win = None
        
        self.load_all_assets()
        self.setup_ui()
        self.add_pet()
        self.main_loop()

    def get_active_window_title(self):
        """Cross-platform active window detection"""
        try:
            if OS_TYPE == "Windows":
                win = gw.getActiveWindow()
                return win.title if win else None
            else:
                # Linux/X11 detection
                d = display.Display()
                root = d.screen().root
                win_id = root.get_full_property(d.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType).value[0]
                win_obj = d.create_resource_object('window', win_id)
                return win_obj.get_wm_name()
        except:
            return None

    def load_all_assets(self):
        img_p, snd_p = "Img/", "soundEffect/"
        sz = (self.size, self.size)
        try:
            self.assets = {
                'normal_l': ImageTk.PhotoImage(Image.open(os.path.join(img_p, "leftNormal.png")).resize(sz)),
                'normal_r': ImageTk.PhotoImage(Image.open(os.path.join(img_p, "rightNormal.png")).resize(sz)),
                'bounce_l': ImageTk.PhotoImage(Image.open(os.path.join(img_p, "leftBounce.png")).resize(sz)),
                'bounce_r': ImageTk.PhotoImage(Image.open(os.path.join(img_p, "rightBounce.png")).resize(sz)),
                's_bounce': pygame.mixer.Sound(os.path.join(snd_p, "bounced.mp3")),
                's_coayo': pygame.mixer.Sound(os.path.join(snd_p, "coayo1.mp3")),
                's_rotate': pygame.mixer.Sound(os.path.join(snd_p, "rotate.mp3"))
            }
        except Exception as e:
            print(f"Error loading assets: {e}"); exit()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#45475a", foreground="white")
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        
        tk.Label(self.root, text="CUAYO COMMANDER", bg="#1e1e2e", fg="#f5c2e7", font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        count_frame = tk.Frame(self.root, bg="#1e1e2e")
        count_frame.pack(pady=10)
        
        tk.Button(count_frame, text=" - ", command=self.remove_pet, bg="#f38ba8", fg="white", width=4).grid(row=0, column=0, padx=10)
        self.lbl_count = tk.Label(count_frame, text="1", bg="#1e1e2e", fg="white", font=("Arial", 14, "bold"))
        self.lbl_count.grid(row=0, column=1)
        tk.Button(count_frame, text=" + ", command=self.add_pet, bg="#a6e3a1", fg="black", width=4).grid(row=0, column=2, padx=10)

        self.btn_mute = tk.Button(self.root, text="MUTE SOUND", command=self.toggle_mute, bg="#89b4fa", width=20)
        self.btn_mute.pack(pady=10)
        
        tk.Label(self.root, text="Speed:").pack(pady=(10,0))
        self.speed_slider = ttk.Scale(self.root, from_=0.5, to=4.0, orient='horizontal', command=self.update_speed)
        self.speed_slider.set(1.0)
        self.speed_slider.pack(fill='x', padx=40, pady=10)

        tk.Button(self.root, text="CLOSE ALL", command=self.root.destroy, bg="#313244", fg="#f38ba8").pack(side="bottom", pady=20)

    def add_pet(self):
        new_pet = SingleCuayo(self.root, self.assets, self.size)
        self.pets.append(new_pet)
        self.lbl_count.config(text=str(len(self.pets)))

    def remove_pet(self):
        if len(self.pets) > 0:
            p = self.pets.pop()
            p.remove()
            self.lbl_count.config(text=str(len(self.pets)))

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        self.btn_mute.config(text="UNMUTE SOUND" if self.is_muted else "MUTE SOUND", bg="#fab387" if self.is_muted else "#89b4fa")

    def update_speed(self, val):
        self.speed_mult = float(val)

    def main_loop(self):
        curr_win = self.get_active_window_title()
        if curr_win and curr_win != self.last_win:
            self.last_win = curr_win
            for p in self.pets: p.trigger_rotate(self.is_muted)

        # Remove dead pets from list
        self.pets = [p for p in self.pets if p.pet_win.winfo_exists()]
        self.lbl_count.config(text=str(len(self.pets)))

        for p in self.pets:
            p.update(self.is_muted, self.speed_mult)
            
        self.root.after(30, self.main_loop)

if __name__ == "__main__":
    root = tk.Tk()
    manager = CuayoManager(root)
    root.mainloop()