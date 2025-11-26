from tkinter import *
from tkinter import messagebox
import sqlite3
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def admin_dashboard(username, name):
    def view_users():
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        cur.execute("SELECT username, name, role FROM login")
        rows = cur.fetchall()
        conn.close()

        top = Toplevel(win)
        top.title("All Users")
        for r in rows:
            Label(top, text=f"Username: {r[0]}, Name: {r[1]}, Role: {r[2]}").pack()

    def register_user():
        def submit():
            try:
                data = (uname.get(), pwd.get(), fullname.get(), role.get())
                conn = sqlite3.connect("DB.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO login VALUES (?, ?, ?, ?)", data)
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "User Registered")
                form.destroy()
            except:
                messagebox.showerror("Error", "Username already exists")

        form = Toplevel(win)
        form.title("Register User")
        uname, pwd, fullname, role = Entry(form), Entry(form), Entry(form), Entry(form)
        labels = ["Username", "Password", "Full Name", "Role (user/police)"]
        for i, lbl in enumerate(labels):
            Label(form, text=lbl).grid(row=i, column=0)
            [uname, pwd, fullname, role][i].grid(row=i, column=1)
        Button(form, text="Submit", command=submit).grid(row=4, column=0, columnspan=2)

    def export_complaints_excel():
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM complaints")
        data = cur.fetchall()
        conn.close()

        wb = Workbook()
        ws = wb.active
        ws.append(["ID", "Username", "Text", "Status", "Date"])
        for row in data:
            ws.append(row)
        wb.save("complaints.xlsx")
        messagebox.showinfo("Exported", "complaints.xlsx created.")

    def export_criminals_pdf():
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM criminals")
        data = cur.fetchall()
        conn.close()

        c = canvas.Canvas("criminals.pdf", pagesize=letter)
        width, height = letter
        y = height - 50
        c.drawString(100, y, "Criminal Records:")
        y -= 20
        for row in data:
            line = ", ".join(str(i) for i in row)
            c.drawString(50, y, line)
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50
        c.save()
        messagebox.showinfo("Exported", "criminals.pdf created.")

    win = Tk()
    win.geometry("400x350")
    win.title("Admin Dashboard")
    Label(win, text=f"Welcome {name}", font=("Arial", 14)).pack(pady=10)

    Button(win, text="View All Users", command=view_users).pack(pady=5)
    Button(win, text="Register New User", command=register_user).pack(pady=5)
    Button(win, text="Export Complaints to Excel", command=export_complaints_excel).pack(pady=5)
    Button(win, text="Export Criminals to PDF", command=export_criminals_pdf).pack(pady=5)
    Button(win, text="Logout", command=win.destroy).pack(pady=20)

    win.mainloop()