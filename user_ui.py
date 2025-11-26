from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime

def user_dashboard(username, name):
    def file_complaint():
        complaint_text = complaint_entry.get("1.0", END).strip()
        if complaint_text:
            conn = sqlite3.connect("DB.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO complaints (username, complaint_text, date) VALUES (?, ?, ?)",
                        (username, complaint_text, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Complaint submitted.")
            complaint_entry.delete("1.0", END)

    def view_complaints():
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        cur.execute("SELECT complaint_id, complaint_text, status, date FROM complaints WHERE username=?", (username,))
        rows = cur.fetchall()
        conn.close()

        top = Toplevel(win)
        top.title("Your Complaints")
        for row in rows:
            Label(top, text=f"ID: {row[0]} | Status: {row[2]} | Date: {row[3]}").pack(anchor='w')
            Label(top, text=row[1], wraplength=380, fg='blue').pack(anchor='w')

    win = Tk()
    win.geometry("500x400")
    win.title("User Dashboard")

    Label(win, text=f"Welcome {name}", font=("Arial", 14)).pack(pady=10)
    Label(win, text="Enter your complaint:").pack()
    complaint_entry = Text(win, height=5, width=50)
    complaint_entry.pack()
    Button(win, text="Submit Complaint", command=file_complaint).pack(pady=10)
    Button(win, text="View My Complaints", command=view_complaints).pack(pady=5)
    Button(win, text="Logout", command=win.destroy).pack(pady=20)
    win.mainloop()