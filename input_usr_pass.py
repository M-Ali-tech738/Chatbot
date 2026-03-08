import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_credentials(file_path, username, hashed_password):
    if not os.path.exists(file_path):
        open(file_path, 'w').close()  # Create the file if it doesn't exist
    with open(file_path, 'a') as f:
        f.write(f"{username},{hashed_password}\n")

def get_credentials(event=None):
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        hashed_password = hash_password(password)
        file_path = '/home/alii/VS Code/Py/main/credentials.txt'  # Specify the file path
        save_credentials(file_path, username, hashed_password)
        messagebox.showinfo("Success", "Credentials saved successfully!")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter both username and password")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        exit()

def main():
    global username_entry, password_entry, window

    window = tk.Tk()
    window.title("Credential Saver")
    window.geometry("300x150")
    window.protocol("WM_DELETE_WINDOW", on_closing)

    style = ttk.Style()
    style.theme_use("clam")

    ttk.Label(window, text="Username").grid(row=0, column=0, padx=10, pady=10)
    username_entry = ttk.Entry(window, width=20)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(window, text="Password").grid(row=1, column=0, padx=10, pady=10)
    password_entry = ttk.Entry(window, width=20, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Button(window, text="Save", command=get_credentials).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    window.bind('<Return>', get_credentials)  # Bind the Enter key to the get_credentials function

    window.mainloop()

if __name__ == "__main__":
    main()
