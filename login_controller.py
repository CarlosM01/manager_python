import os
import tkinter as tk
from tkinter import messagebox
from ui import LoginWindow, RegisterWindow
from api_request import Api

class LoginController:
    def __init__(self):
        self.token = None
        api_url = os.getenv('API_URL', 'http://localhost:8080/')
        self.register_url = f"{api_url}auth/register/"
        self.login_url = f"{api_url}auth/login/"
        self.profile_url = f"{api_url}auth/profile/"
        self.login_window = None
        self.register_window = None
        self.show_login_window()

    def show_login_window(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()

    def show_register_window(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()

    def verify_user(self):
        username = self.login_window.username_entry.get()
        password = self.login_window.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Error", "Please enter both username and password")
            return

        data = {"username": username, "password": password}

        try:
            res = Api.post(self.login_url, data)
            if res.get("success"):
                self.token = res["token"]
                messagebox.showinfo("Success", "Login successful")
                self.login_window.destroy()
                self.show_profile_window()
            else:
                error_message = res.get("error", "Unknown error")
                messagebox.showerror("Login Error", error_message)
        except Exception as e:
            messagebox.showerror("Critical Error", f"Unexpected error: {str(e)}")

    def register_user(self):
        username = self.register_window.register_username_entry.get()
        email = self.register_window.register_email_entry.get()
        password = self.register_window.register_password_entry.get()
        confirm_password = self.register_window.register_confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showwarning("Error", "All fields are required")
            return
        if password != confirm_password:
            messagebox.showwarning("Error", "Passwords do not match")
            return

        data = {"username": username, "email": email, "password": password, "role": "user"}

        try:
            res = Api.post(self.register_url, data)
            if res.get("success"):
                messagebox.showinfo("Success", "User registered successfully")
                self.register_window.destroy()
            else:
                error_message = res.get("error", "Unknown error")
                messagebox.showerror("Registration Error", error_message)
        except Exception as e:
            messagebox.showerror("Critical Error", f"Unexpected error: {str(e)}")

    def show_profile_window(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            res = Api.get(self.profile_url, headers=headers)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch profile: {str(e)}")
            return

        if "error" in res:
            messagebox.showerror("Error", res["error"])
            return

        profile_window = tk.Tk()
        profile_window.title("User Profile")
        profile_window.geometry("400x300")

        tk.Label(profile_window, text="Access Granted", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(profile_window, text=f"Username: {res.get('username', 'N/A')}", font=("Arial", 12)).pack(pady=5)
        tk.Label(profile_window, text=f"Email: {res.get('email', 'N/A')}", font=("Arial", 12)).pack(pady=5)
        tk.Label(profile_window, text=f"Role: {res.get('role', 'N/A')}", font=("Arial", 12)).pack(pady=5)

        tk.Button(profile_window, text="Logout", font=("Arial", 12), command=lambda: self.logout(profile_window)).pack(pady=20)

        profile_window.mainloop()

    def logout(self, profile_window):
        self.token = None
        profile_window.destroy()
        self.show_login_window()