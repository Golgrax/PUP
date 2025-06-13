# shop_app/main.py
import tkinter as tk
from tkinter import font
import threading
from tkinterweb import HtmlFrame
from PIL import Image, ImageTk
import os

# Import the Flask app instance and the run function
from .web_server import run_shop_server

FLAG_FILE = os.path.join(os.path.dirname(__file__), 'first_run.flag')

class PUPShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PUP E-Commerce")
        self.root.geometry("450x850")
        self.root.resizable(False, False)

        # Check for first run
        if not os.path.exists(FLAG_FILE):
            self.show_splash_screens()
        else:
            self.setup_main_ui()

    def show_splash_screens(self):
        self.splash_frame = tk.Frame(self.root, bg="white")
        self.splash_frame.pack(fill="both", expand=True)
        self.splash_screens = []
        self.current_splash = 0

        # Create 3 splash screens
        for i in range(3):
            frame = tk.Frame(self.splash_frame, bg="#722F37")
            lbl = tk.Label(frame, text=f"Welcome to PUP Shop!\nScreen {i+1}", font=("Arial", 24, "bold"), fg="white", bg="#722F37")
            lbl.pack(pady=100)
            self.splash_screens.append(frame)
        
        # Navigation buttons for splash
        nav_frame = tk.Frame(self.splash_frame, bg="#722F37")
        nav_frame.pack(side="bottom", fill="x", pady=20)
        
        self.back_btn = tk.Button(nav_frame, text="Back", command=self.prev_splash, bg="#FFD700")
        self.next_btn = tk.Button(nav_frame, text="Next", command=self.next_splash, bg="#FFD700")
        self.start_btn = tk.Button(nav_frame, text="Get Started", command=self.start_app, bg="#4CAF50", fg="white")

        self.back_btn.pack(side="left", padx=20)
        self.next_btn.pack(side="right", padx=20)
        
        self.update_splash_view()

    def update_splash_view(self):
        for frame in self.splash_screens:
            frame.pack_forget() # Hide all
        self.splash_screens[self.current_splash].pack(fill="both", expand=True) # Show current
        
        self.back_btn.pack(side="left", padx=20)
        self.next_btn.pack(side="right", padx=20)
        self.start_btn.pack_forget()
        
        self.back_btn['state'] = 'normal' if self.current_splash > 0 else 'disabled'
        
        if self.current_splash == len(self.splash_screens) - 1:
            self.next_btn.pack_forget()
            self.start_btn.pack(side="right", padx=20)
            
    def next_splash(self):
        if self.current_splash < len(self.splash_screens) - 1:
            # Animate: slide out left, slide in from right
            old_frame = self.splash_screens[self.current_splash]
            self.current_splash += 1
            new_frame = self.splash_screens[self.current_splash]
            
            old_frame.place(x=0, y=0, relwidth=1, relheight=1)
            new_frame.place(x=self.root.winfo_width(), y=0, relwidth=1, relheight=1)
            
            self.slide_animation(old_frame, new_frame, "left")

    def prev_splash(self):
        if self.current_splash > 0:
            old_frame = self.splash_screens[self.current_splash]
            self.current_splash -= 1
            new_frame = self.splash_screens[self.current_splash]

            old_frame.place(x=0, y=0, relwidth=1, relheight=1)
            new_frame.place(x=-self.root.winfo_width(), y=0, relwidth=1, relheight=1)

            self.slide_animation(old_frame, new_frame, "right")
            
    def slide_animation(self, old_frame, new_frame, direction):
        width = self.root.winfo_width()
        pos_old, pos_new = 0, width if direction == "left" else -width
        
        step = int(width / 20)
        if direction == "left":
            end_old, end_new = -width, 0
            step = -step
        else: # right
            end_old, end_new = width, 0

        def animate():
            nonlocal pos_old, pos_new
            pos_old += step
            pos_new += step
            
            old_frame.place_configure(x=pos_old)
            new_frame.place_configure(x=pos_new)
            
            if (direction == "left" and pos_new > 0) or (direction == "right" and pos_new < 0):
                self.root.after(10, animate)
            else:
                old_frame.place_forget()
                new_frame.place(x=0, y=0, relwidth=1, relheight=1)
                new_frame.pack(fill="both", expand=True)
                self.update_splash_view()
        
        animate()

    def start_app(self):
        # Create the flag file so splash doesn't show again
        with open(FLAG_FILE, 'w') as f:
            f.write('ran')
        self.splash_frame.destroy()
        self.setup_main_ui()

    def setup_main_ui(self):
        self.webview = HtmlFrame(self.root, messages_enabled=False)
        self.webview.pack(fill="both", expand=True)
        # Load the main page from the Flask server
        self.webview.load_url("http://127.0.0.1:5000")

def main():
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_shop_server, daemon=True)
    flask_thread.start()

    # Start the Tkinter GUI
    root = tk.Tk()
    app = PUPShopApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()