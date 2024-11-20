import os
import tkinter as tk
from tkinter import messagebox
from ui import LoginWindow, RegisterWindow, UpdateWindow
from api_request import Api

class Controller:
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

    def logout(self, profile_window):
        # Limpiar el token de autenticación
        self.token = None
        
        # Cerrar la ventana del perfil
        profile_window.destroy()
        
        # Mostrar la ventana de inicio de sesión
        self.show_login_window()


    def show_register_window(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()

    def show_update_window(self, user_data):
        self.update_window = UpdateWindow(self, user_data)
        self.update_window.show()

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
            if res.get("userId"):
                messagebox.showinfo("success","Usuario registrado")
                self.register_window.destroy()
            else:
                error_message = res.get("error", "Unknown error")
                messagebox.showerror("Registration Error", error_message)
        except Exception as e:
            messagebox.showerror("Critical Error", f"Unexpected error: {str(e)}")

    def update_user(self):
        # Obtener los nuevos datos ingresados por el usuario
        username = self.update_window.update_username_entry.get()
        email = self.update_window.update_email_entry.get()
        password = self.update_window.update_password_entry.get()
        confirm_password = self.update_window.update_confirm_password_entry.get()

        # Validar que las contraseñas coincidan si se han proporcionado
        if password and confirm_password and password != confirm_password:
            messagebox.showwarning("Error", "Passwords do not match")
            return

        # Preparar los datos para enviar solo si están completos
        data = {}

        if username:
            data["username"] = username
        if email:
            data["email"] = email
        if password:
            data["password"] = password

        # Si no hay datos para enviar, mostrar advertencia
        if not data:
            messagebox.showwarning("Error", "No data to update")
            return

        # Llamar a la API para actualizar los datos
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            res = Api.put(self.profile_url, data, headers=headers)

            if res.get("message"):
                messagebox.showinfo("Success", res.get('message'))
                self.update_window.destroy()  # Cerrar la ventana de actualización
                self.logout(self.profile_window)
            else:
                error_message = res.get("error", "Unknown error")
                messagebox.showerror("Update Error", error_message)

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

        self.profile_window = tk.Tk()
        self.profile_window.title("User Profile")
        self.profile_window.geometry("400x400")

        # Mostrar los detalles del perfil
        tk.Label(self.profile_window, text="Access Granted", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.profile_window, text=f"Username: {res.get('username', 'N/A')}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.profile_window, text=f"Email: {res.get('email', 'N/A')}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.profile_window, text=f"Role: {res.get('role', 'N/A')}", font=("Arial", 12)).pack(pady=5)

        # Botón para cambiar los datos del usuario
        def open_update_window():
            self.show_update_window(user_data=res)  # Pasar los datos del usuario para que se autocompleten

        tk.Button(self.profile_window, text="Update Profile", font=("Arial", 12), command=open_update_window).pack(pady=10)

        # Botón para eliminar el usuario
        def delete_account():
            result = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account?")
            if result:
                try:
                    res = Api.delete(self.profile_url, headers=headers)
                    if res.get("message"):
                        messagebox.showinfo("Success", res.get("message"))
                        self.logout(self.profile_window)  # Cerrar sesión después de eliminar la cuenta
                    else:
                        error_message = res.get("error", "Unknown error")
                        messagebox.showerror("Deletion Error", error_message)
                except Exception as e:
                    messagebox.showerror("Critical Error", f"Unexpected error: {str(e)}")

        tk.Button(self.profile_window, text="Delete Account", font=("Arial", 12), command=delete_account).pack(pady=10)

        # Botón para cerrar sesión
        tk.Button(self.profile_window, text="Logout", font=("Arial", 12), command=lambda: self.logout(self.profile_window)).pack(pady=20)

        self.profile_window.mainloop()