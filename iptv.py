import tkinter as tk
from tkinter import messagebox
import json
import os
import webview

SETTINGS_FILE = "settings.json"
BASE_URL = "http://iptv.moojafzar.com/s/?mmk"

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IPTV Login")
        self.key_press_count = 0

        # ---------- Login UI ----------
        self.frm_login = tk.Frame(self.root)
        self.frm_login.pack(pady=10)

        tk.Label(self.frm_login, text="Username:").pack()
        self.txt_user = tk.Entry(self.frm_login)
        self.txt_user.pack()

        tk.Label(self.frm_login, text="Password:").pack()
        self.txt_pass = tk.Entry(self.frm_login, show="*")
        self.txt_pass.pack()

        tk.Button(self.frm_login, text="Login", command=self.login).pack(pady=5)

        # load previous settings
        self.load_settings()
        self.root.bind("<Key>", self.secret_key)

        self.root.geometry("400x200")
        self.root.mainloop()

    # ---------- Settings ----------
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    s = json.load(f)
                    self.txt_user.insert(0, s.get("username", ""))
                    self.txt_pass.insert(0, s.get("password", ""))
            except:
                pass

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "username": self.txt_user.get(),
                "password": self.txt_pass.get()
            }, f)

    # ---------- URL Builder ----------
    def build_url(self):
        user = self.txt_user.get().strip()
        pas = self.txt_pass.get().strip()

        # هیچ یوزر و پسورد وارد نشده
        if user == "" and pas == "":
            return f"{BASE_URL}&u=&p="

        # فقط یوزر وارد شده
        if user != "" and pas == "":
            return f"{BASE_URL}&u={user}&p="

        # هر دو وارد شده‌اند
        return f"{BASE_URL}&u={user}&p={pas}"

    # ---------- Login ----------
    def login(self):
        url = self.build_url()
        self.save_settings()

        # remove the login window
        self.frm_login.pack_forget()

        try:
            webview.create_window("IPTV", url, width=900, height=600, fullscreen=True)
            webview.start()
        except Exception as e:
            messagebox.showerror("Error loading site", str(e))

    # ---------- Secret Key ----------
    def secret_key(self, event):
        if event.keysym == "Up":
            self.key_press_count += 1
            if self.key_press_count >= 9:
                messagebox.showinfo("Secret", "Hidden settings unlocked!")
                self.key_press_count = 0
        else:
            self.key_press_count = 0


if __name__ == "__main__":
    App()
