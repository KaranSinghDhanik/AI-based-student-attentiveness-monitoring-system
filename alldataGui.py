import tkinter as tk
from tkinter import ttk
import sqlite3

# --- Parameters ---
THRESHOLD = 60  # Score above this is considered 'attentive'
TIME_PER_ENTRY = 1  # Assume each row = 1 second

# --- Functions ---
def fetch_data(selected_user=None):
    conn = sqlite3.connect("attentiveness.db")
    cursor = conn.cursor()
    if selected_user and selected_user != "All":
        cursor.execute("SELECT id, name, timestamp, lip_status, eye_status, head_status, lip_score, eye_score, head_score, final_score FROM full_attentiveness WHERE name=? ORDER BY id DESC", (selected_user,))
    else:
        cursor.execute("SELECT id, name, timestamp, lip_status, eye_status, head_status, lip_score, eye_score, head_score, final_score FROM full_attentiveness ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_usernames():
    conn = sqlite3.connect("attentiveness.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM full_attentiveness")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

def calculate_summary(data):
    if not data:
        return 0, 0, 0, 0.0
    total_entries = len(data)
    total_points = sum(row[-1] for row in data)  # final_score
    attentive_entries = sum(1 for row in data if row[-1] >= THRESHOLD)
    total_time = total_entries * TIME_PER_ENTRY
    attentive_time = attentive_entries * TIME_PER_ENTRY
    avg_score = round(total_points / total_entries, 2)
    return total_time, attentive_time, total_points, avg_score

def populate_tree(tree, data):
    for row in tree.get_children():
        tree.delete(row)
    for entry in data:
        tree.insert('', 'end', values=entry)

def refresh_data():
    selected_user = user_var.get()
    data = fetch_data(selected_user)
    populate_tree(tree, data)
    total_time, attentive_time, total_points, avg_score = calculate_summary(data)
    avg_label.config(text=f"Average Attentiveness: {avg_score}%")
    points_label.config(text=f"Attentive Points: {round(total_points, 2)}")
    time_label.config(text=f"Total Time: {total_time} sec | Attentive Time: {attentive_time} sec")

# --- GUI Setup ---
root = tk.Tk()
root.title("Attentiveness Logs Viewer")
root.geometry("1200x600")

columns = ('ID', 'Name', 'Timestamp', 'Lip Status', 'Eye Status', 'Head Status',
           'Lip Score', 'Eye Score', 'Head Score', 'Final Score')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center')
tree.pack(expand=True, fill='both', padx=10, pady=10)

# User filter
user_var = tk.StringVar()
usernames = ["All"] + fetch_usernames()
user_var.set("All")
user_menu = ttk.OptionMenu(root, user_var, *usernames, command=lambda _: refresh_data())
user_menu.pack(pady=5)

avg_label = tk.Label(root, text="Average Attentiveness: --%", font=('Helvetica', 14, 'bold'))
avg_label.pack(pady=5)

points_label = tk.Label(root, text="Attentive Points: --", font=('Helvetica', 12))
points_label.pack(pady=2)

time_label = tk.Label(root, text="Total Time: -- sec | Attentive Time: -- sec", font=('Helvetica', 12))
time_label.pack(pady=2)

refresh_btn = tk.Button(root, text="Refresh Data", command=refresh_data, font=('Helvetica', 12))
refresh_btn.pack(pady=10)

# Load initially
refresh_data()
root.mainloop()