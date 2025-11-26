from tkinter import *
from tkinter import messagebox
import sqlite3

def police_dashboard(username, name):
    def view_complaints():
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        cur.execute("SELECT complaint_id, username, complaint_text, status FROM complaints")
        rows = cur.fetchall()
        conn.close()

        top = Toplevel(win)
        top.title("All Complaints")
        for row in rows:
            Label(top, text=f"ID: {row[0]} | User: {row[1]} | Status: {row[3]}").pack(anchor='w')
            Label(top, text=row[2], wraplength=380, fg='blue').pack(anchor='w')
            status_entry = Entry(top)
            status_entry.pack()
            Button(top, text="Update Status", command=lambda cid=row[0], e=status_entry: update_status(cid, e.get())).pack()

    def update_status(cid, new_status):
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        cur.execute("UPDATE complaints SET status=? WHERE complaint_id=?", (new_status, cid))
        conn.commit()
        conn.close()
        messagebox.showinfo("Updated", f"Status updated for ID {cid}")

    def add_criminal():
        def submit():
            data = (cid.get(), cname.get(), age.get(), gender.get(), crime.get(), status.get())
            conn = sqlite3.connect("DB.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO criminals VALUES (?, ?, ?, ?, ?, ?)", data)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Criminal added.")
            form.destroy()

        form = Toplevel(win)
        form.title("Add Criminal")
        cid, cname, age, gender, crime, status = Entry(form), Entry(form), Entry(form), Entry(form), Entry(form), Entry(form)
        labels = ["ID", "Name", "Age", "Gender", "Crime", "Status"]
        for i, lbl in enumerate(labels):
            Label(form, text=lbl).grid(row=i, column=0)
            [cid, cname, age, gender, crime, status][i].grid(row=i, column=1)
        Button(form, text="Submit", command=submit).grid(row=6, column=0, columnspan=2)

    def search_criminal():
        def do_search():
            term = search_entry.get()
            conn = sqlite3.connect("DB.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM criminals WHERE name LIKE ? OR criminal_id LIKE ?", (f"%{term}%", f"%{term}%"))
            rows = cur.fetchall()
            conn.close()

            result = Toplevel(win)
            result.title("Search Results")
            for r in rows:
                Label(result, text=", ".join(str(x) for x in r)).pack(anchor='w')

        search_win = Toplevel(win)
        search_win.title("Search Criminal")
        search_entry = Entry(search_win, width=40)
        search_entry.pack(pady=5)
        Button(search_win, text="Search", command=do_search).pack()

    win = Tk()
    win.geometry("500x350")
    win.title("Police Dashboard")
    Label(win, text=f"Welcome {name}", font=("Arial", 14)).pack(pady=10)

    Button(win, text="View Complaints", command=view_complaints).pack(pady=5)
    Button(win, text="Add Criminal", command=add_criminal).pack(pady=5)
    Button(win, text="Search Criminal", command=search_criminal).pack(pady=5)
    Button(win, text="Logout", command=win.destroy).pack(pady=20)
    win.mainloop()