import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import bcrypt
from PIL import Image, ImageTk  # Import PIL for image handling
import dashboard


# Database Connection
def connect_db():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password BLOB
        )
    """)
    conn.commit()
    conn.close()

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eazy-Shop Login")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        # Ensure Database Exists
        connect_db()

        # Load Image Path
        self.image_path = "bag.png"
        self.bg_image = None  # Placeholder for the image

        # Create a Label for the Background
        self.bg_label = tk.Label(self.root)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Load and Resize Background Image
        self.load_background_image()

        # Bind window resize event
        self.root.bind("<Configure>", self.resize_background)

        # Login Frame
        self.login_frame = tk.Frame(root, bg="white", padx=20, pady=20)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(self.login_frame, text="Eazy-Shop", font=("Arial", 24, "bold"), bg="white").pack(pady=10)

        # Email Input
        tk.Label(self.login_frame, text="Email:", font=("Arial", 14, "bold"), bg="white").pack()
        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 14), width=30, bg="lightgrey")
        self.username_entry.pack(pady=5)

        # Password Input
        tk.Label(self.login_frame, text="Password:", font=("Arial", 14, "bold"), bg="white").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 14), width=30, bg="lightcoral")
        self.password_entry.pack(pady=5)

        # Login Button
        tk.Button(self.login_frame, text="Sign In", font=("Arial", 14, "bold"), bg="white", command=self.login).pack(pady=10)

        # Sign Up Button
        tk.Button(self.login_frame, text="Sign Up", font=("Arial", 14, "bold"), bg="lightgrey", command=self.signup).pack()

        # Tagline
        tk.Label(root, text="A NEW APPROACH TO SHOPPING", font=("Arial", 16, "bold"), bg="white").place(relx=0.5, rely=0.9, anchor="center")

    def load_background_image(self):
        """Loads and resizes the background image."""
        if os.path.exists(self.image_path):
            original_image = Image.open(self.image_path)
            resized_image = original_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_image)
            self.bg_label.config(image=self.bg_image)
        else:
            messagebox.showwarning("Image Missing", "Background image not found!")

    def resize_background(self, event=None):
        """Resizes the background image when the window size changes."""
        if self.bg_image:
            original_image = Image.open(self.image_path)
            resized_image = original_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_image)
            self.bg_label.config(image=self.bg_image)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode('utf-8')

        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user[0]):
            messagebox.showinfo("Login Successful", "Welcome to Eazy-Shop!")
            self.root.destroy()  # Close login window
            dashboard.Dashboard(username)  # Open Dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    def signup(self):
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Sign Up")
        self.signup_window.geometry("400x300")

        tk.Label(self.signup_window, text="Create Account", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.signup_window, text="Email:", font=("Arial", 12)).pack()
        self.signup_username_entry = tk.Entry(self.signup_window, font=("Arial", 12))
        self.signup_username_entry.pack()

        tk.Label(self.signup_window, text="Password:", font=("Arial", 12)).pack()
        self.signup_password_entry = tk.Entry(self.signup_window, show="*", font=("Arial", 12))
        self.signup_password_entry.pack()

        tk.Button(self.signup_window, text="Register", font=("Arial", 12, "bold"), bg="lightblue",
                  command=self.register_user).pack(pady=10)

    def register_user(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get().encode('utf-8')

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        try:
            conn = sqlite3.connect("ecommerce.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully!")
            self.signup_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")

# Start the application
def main():
    login_root = tk.Tk()
    LoginApp(login_root)
    login_root.mainloop()

if __name__ == "__main__":
    main()
