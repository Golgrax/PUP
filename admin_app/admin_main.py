# admin_app/admin_main.py
import tkinter as tk
import threading
from tkinterweb import HtmlFrame

# Import the admin Flask app and run function
from .admin_web_server import run_admin_server

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PUP Shop - Admin Panel")
        self.root.geometry("800x600")

        self.webview = HtmlFrame(self.root, messages_enabled=False)
        self.webview.pack(fill="both", expand=True)
        self.webview.load_url("http://127.0.0.1:5001")

def main():
    # Start the Admin Flask server in a separate thread
    flask_thread = threading.Thread(target=run_admin_server, daemon=True)
    flask_thread.start()

    # Start the Tkinter GUI
    root = tk.Tk()
    app = AdminApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()