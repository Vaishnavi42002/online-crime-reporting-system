from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from user_ui import user_dashboard
from police_ui import police_dashboard
from admin_ui import admin_dashboard

def start_login():
    def login():
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        uname = username_entry.get()
        pwd = password_entry.get()
        cur.execute("SELECT password, role, name FROM login WHERE username=?", (uname,))
        result = cur.fetchone()
        conn.close()
        if result and result[0] == pwd:
            role = result[1]
            name = result[2]
            root.destroy()
            if role == 'user':
                user_dashboard(uname, name)
            elif role == 'police':
                police_dashboard(uname, name)
            elif role == 'admin':
                admin_dashboard(uname, name)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_register():
        reg = Toplevel(root)
        reg.title("Register Account")
        reg.geometry("400x300")

        Label(reg, text="Full Name").pack()
        name_entry = Entry(reg)
        name_entry.pack()

        Label(reg, text="Username").pack()
        uname_entry = Entry(reg)
        uname_entry.pack()

        Label(reg, text="Password").pack()
        pwd_entry = Entry(reg, show="*")
        pwd_entry.pack()

        Label(reg, text="Select Role").pack()
        role_var = StringVar()
        role_combo = ttk.Combobox(reg, textvariable=role_var, state="readonly")
        role_combo['values'] = ('user', 'police')
        role_combo.pack()

        def register_user():
            name = name_entry.get().strip()
            uname = uname_entry.get().strip()
            pwd = pwd_entry.get().strip()
            role = role_var.get()
            if role not in ['user', 'police']:
                messagebox.showerror("Error", "Please select a valid role.")
                return
            try:
                conn = sqlite3.connect("DB.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO login VALUES (?, ?, ?, ?)", (uname, pwd, name, role))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Registered successfully!")
                reg.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")

        Button(reg, text="Register", command=register_user).pack(pady=20)

    root = Tk()
    root.geometry("400x300")
    root.title("Login - Crime Reporting System")

    Label(root, text="Username").pack(pady=10)
    username_entry = Entry(root)
    username_entry.pack()

    Label(root, text="Password").pack(pady=10)
    password_entry = Entry(root, show="*")
    password_entry.pack()

    Button(root, text="Login", command=login).pack(pady=10)
    Button(root, text="Register (User/Police)", command=open_register).pack()

    root.mainloop()
