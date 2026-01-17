import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import subprocess
import sqlite3

DB_PATH = "attentiveness.db"

class AttentivenessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attentiveness Monitor")
        self.username = None
        self.main_frame = None
        self.login_screen()

    def login_screen(self):
        if self.main_frame:
            self.main_frame.destroy()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)
        tk.Label(self.main_frame, text="Enter your name:", font=("Arial", 14)).pack()
        self.name_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.name_entry.pack(pady=10)
        tk.Button(self.main_frame, text="Login", command=self.do_login, font=("Arial", 12)).pack()

    def do_login(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        self.username = name
        self.show_main_menu()

    def show_main_menu(self):
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)
        tk.Label(self.main_frame, text=f"Welcome, {self.username}!", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Start Monitoring", command=self.start_monitoring, width=25, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.main_frame, text="View My Data", command=self.view_my_data, width=25, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.main_frame, text="Delete My Data", command=self.delete_my_data, width=25, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.login_screen, width=25, font=("Arial", 12)).pack(pady=5)

    def start_monitoring(self):
        try:
            subprocess.run(["python", "combined.py", self.username])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {e}")

    def view_my_data(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, lip_status, eye_status, head_status, final_score FROM full_attentiveness WHERE name=?", (self.username,))
        rows = cursor.fetchall()
        conn.close()
        view_win = tk.Toplevel(self.root)
        view_win.title("My Attentiveness Data")
        cols = ["Timestamp", "Lip", "Eye", "Head", "Final Score"]
        tree = ttk.Treeview(view_win, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True)
        tk.Button(view_win, text="Close", command=view_win.destroy).pack(pady=5)

    def delete_my_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all your data?"):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM full_attentiveness WHERE name=?", (self.username,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Your data has been deleted.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttentivenessApp(root)
    root.mainloop()