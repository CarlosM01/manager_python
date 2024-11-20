import tkinter as tk

class Window:
    def __init__(self, title, size):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(size)

    def show(self):
        self.window.mainloop()

    def destroy(self):
        self.window.destroy()

class LoginWindow(Window):
    def __init__(self, controller):
        super().__init__("Login", "400x300")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Username:", font=("Arial", 12)).pack(pady=10)
        self.username_entry = tk.Entry(self.window, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="Password:", font=("Arial", 12)).pack(pady=10)
        self.password_entry = tk.Entry(self.window, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        tk.Button(self.window, text="Login", font=("Arial", 12), command=self.controller.verify_user).pack(pady=20)
        tk.Button(self.window, text="Register", font=("Arial", 12), command=self.controller.show_register_window).pack(pady=20)

class RegisterWindow(Window):
    def __init__(self, controller):
        super().__init__("User Registration", "400x400")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.register_username_entry = tk.Entry(self.window, font=("Arial", 12))
        self.register_username_entry.pack(pady=5)

        tk.Label(self.window, text="Email:", font=("Arial", 12)).pack(pady=5)
        self.register_email_entry = tk.Entry(self.window, font=("Arial", 12))
        self.register_email_entry.pack(pady=5)

        tk.Label(self.window, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.register_password_entry = tk.Entry(self.window, show="*", font=("Arial", 12))
        self.register_password_entry.pack(pady=5)

        tk.Label(self.window, text="Confirm Password:", font=("Arial", 12)).pack(pady=5)
        self.register_confirm_password_entry = tk.Entry(self.window, show="*", font=("Arial", 12))
        self.register_confirm_password_entry.pack(pady=5)

        tk.Button(self.window, text="Register", font=("Arial", 12), command=self.controller.register_user).pack(pady=20)

class UpdateWindow(Window):
    def __init__(self, controller, user_data):
        super().__init__("Update User Data", "400x400")
        self.controller = controller
        self.user_data = user_data
        self.create_widgets()

    def create_widgets(self):
        # Username (pre-cargar con el valor actual)
        tk.Label(self.window, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.update_username_entry = tk.Entry(self.window, font=("Arial", 12))
        self.update_username_entry.insert(0, self.user_data.get("username", ""))
        self.update_username_entry.pack(pady=5)

        # Email (pre-cargar con el valor actual)
        tk.Label(self.window, text="Email:", font=("Arial", 12)).pack(pady=5)
        self.update_email_entry = tk.Entry(self.window, font=("Arial", 12))
        self.update_email_entry.insert(0, self.user_data.get("email", ""))
        self.update_email_entry.pack(pady=5)

        # New Password
        tk.Label(self.window, text="New Password:", font=("Arial", 12)).pack(pady=5)
        self.update_password_entry = tk.Entry(self.window, show="*", font=("Arial", 12))
        self.update_password_entry.pack(pady=5)

        # Confirm New Password
        tk.Label(self.window, text="Confirm New Password:", font=("Arial", 12)).pack(pady=5)
        self.update_confirm_password_entry = tk.Entry(self.window, show="*", font=("Arial", 12))
        self.update_confirm_password_entry.pack(pady=5)

        # Button to submit the update
        tk.Button(self.window, text="Update", font=("Arial", 12), command=self.controller.update_user).pack(pady=20)
