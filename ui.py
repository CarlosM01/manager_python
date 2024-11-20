import os
import tkinter as tk
from tkinter import messagebox
from api_request import Api

class LoginApp:
    def __init__(self):
        self.token = None
        api_url = os.getenv('API_URL', 'http://localhost:8080/')
        self.register_url = f"{api_url}auth/register/"
        self.login_url = f"{api_url}auth/login/"
        self.profile_url = f"{api_url}auth/profile/"
        print(api_url, self.register_url, self.login_url, self.profile_url, sep='\n')
        self.show_login_window()

    def show_login_window(self):
        # Main login window
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.login_window.geometry("400x300")

        # Username field
        tk.Label(self.login_window, text="Username:", font=("Arial", 12)).pack(pady=10)
        self.username_entry = tk.Entry(self.login_window, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        # Password field
        tk.Label(self.login_window, text="Password:", font=("Arial", 12)).pack(pady=10)
        self.password_entry = tk.Entry(self.login_window, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        # Buttons
        tk.Button(self.login_window, text="Login", font=("Arial", 12), command=self.verify_user).pack(pady=20)
        tk.Button(self.login_window, text="Register", font=("Arial", 12), command=self.show_register_window).pack(pady=20)

        self.login_window.mainloop()

    def show_register_window(self):
        # Registration window
        self.register_window = tk.Tk()
        self.register_window.title("User Registration")
        self.register_window.geometry("400x400")

        # Username field
        tk.Label(self.register_window, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.register_username_entry = tk.Entry(self.register_window, font=("Arial", 12))
        self.register_username_entry.pack(pady=5)

        # Username field
        tk.Label(self.register_window, text="Email:", font=("Arial", 12)).pack(pady=5)
        self.register_email_entry = tk.Entry(self.register_window, font=("Arial", 12))
        self.register_email_entry.pack(pady=5)

        # Password field
        tk.Label(self.register_window, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.register_password_entry = tk.Entry(self.register_window, show="*", font=("Arial", 12))
        self.register_password_entry.pack(pady=5)

        # Confirm password field
        tk.Label(self.register_window, text="Confirm Password:", font=("Arial", 12)).pack(pady=5)
        self.register_confirm_password_entry = tk.Entry(self.register_window, show="*", font=("Arial", 12))
        self.register_confirm_password_entry.pack(pady=5)

        # Register button
        tk.Button(self.register_window, text="Register", font=("Arial", 12), command=self.register_user).pack(pady=20)

        self.register_window.mainloop()

    def register_user(self):
        username = self.register_username_entry.get()
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.register_confirm_password_entry.get()

        # Field validation
        if not username or not password or not confirm_password:
            messagebox.showwarning("Error", "All fields are required")
            return
        if password != confirm_password:
            messagebox.showwarning("Error", "Passwords do not match")
            return

        # API data
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

    def verify_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

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

        # Profile window
        profile_window = tk.Tk()
        profile_window.title("User Profile")
        profile_window.geometry("400x300")

        # Display user info
        tk.Label(profile_window, text="Access Granted", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(profile_window, text=f"Username: {res.get('username', 'N/A')}", font=("Arial", 12)).pack(pady=5)
        tk.Label(profile_window, text=f"Email: {res.get('email', 'N/A')}", font=("Arial", 12)).pack(pady=5)
        tk.Label(profile_window, text=f"Role: {res.get('role', 'N/A')}", font=("Arial", 12)).pack(pady=5)

        # Logout button
        tk.Button(profile_window, text="Logout", font=("Arial", 12), command=lambda: self.logout(profile_window)).pack(pady=20)

        profile_window.mainloop()

    def logout(self, profile_window):
        self.token = None
        profile_window.destroy()
        self.show_login_window()


# Run the app
if __name__ == "__main__":
    LoginApp()
