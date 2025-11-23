"""
Study Buddy — Forest Edition (MySQL backend)
Requirements:
  pip install mysql-connector-python
MySQL DB (as provided by the user):
  host=localhost
  user=root
  password=1234
  database=study_buddy
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random, os
import mysql.connector
from datetime import datetime

# -------------------------
# MySQL configuration
# -------------------------
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "study_buddy",
    "autocommit": False
}

# -------------------------
# DB helpers
# -------------------------
def get_db_connection():
    """Return a new MySQL connection using MYSQL_CONFIG.
       Shows a messagebox and raises on failure.
    """
    try:
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"]
        )
        return conn
    except mysql.connector.Error as e:
        # If GUI root exists, show error using messagebox, else print
        try:
            messagebox.showerror("Database Connection Error", f"Could not connect to MySQL:\n{e}")
        except Exception:
            print("DB connection error:", e)
        raise

def init_db():
    """Create tables tasks and brain_fog if they don't exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    # tasks table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(1024) NOT NULL,
        deadline VARCHAR(128) DEFAULT 'No deadline',
        completed TINYINT(1) DEFAULT 0
    ) ENGINE=InnoDB;
    """)
    # brain_fog table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS brain_fog (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date VARCHAR(50),
        focus INT,
        sleepiness INT,
        understanding INT,
        memory INT,
        stress INT,
        score INT,
        fog_level VARCHAR(64)
    ) ENGINE=InnoDB;
    """)
    conn.commit()
    cur.close()
    conn.close()

# -------------------------
# DB CRUD
# -------------------------
def save_task_db(task_text, deadline_text):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO tasks (task, deadline, completed) VALUES (%s, %s, %s)",
                    (task_text, deadline_text or "No deadline", 0))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def load_tasks_db():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id, task, deadline, completed FROM tasks ORDER BY id ASC")
        rows = cur.fetchall()
        # rows are list of dicts
        return rows
    finally:
        cur.close()
        conn.close()

def update_task_completed_db(task_id, completed_bool):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE tasks SET completed = %s WHERE id = %s", (1 if completed_bool else 0, task_id))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_completed_db():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE completed = 1")
        conn.commit()
    finally:
        cur.close()
        conn.close()

def save_brain_fog_db(date_str, focus, sleepiness, understanding, memory, stress, score, fog_level):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO brain_fog
            (date, focus, sleepiness, understanding, memory, stress, score, fog_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (date_str, focus, sleepiness, understanding, memory, stress, score, fog_level))
        conn.commit()
    finally:
        cur.close()
        conn.close()

# -------------------------
# Sample Data & Globals
# -------------------------
QUOTES = [
    "Like a tree, grow a little every day.",
    "Every forest starts with a single seed.",
    "Stay grounded, but keep reaching upward.",
    "Calm mind, steady progress.",
    "You’re growing beautifully. Keep going!"
]

EXERCISES = [
    {"exercise": "17 + 26 = ?", "answer": "43"},
    {"exercise": "25 * 4 = ?", "answer": "100"},
    {"exercise": "150 ÷ 3 = ?", "answer": "50"},
    {"exercise": "45 - 12 = ?", "answer": "33"},
    {"exercise": "Word from 'RAP'? (3 letters)", "answer": "PAR"}
]

used_exercises = []

# -------------------------
# App logic (UI callbacks)
# -------------------------
def motivate():
    messagebox.showinfo("Grow Strong 🌿", random.choice(QUOTES))

def mini_exercise():
    global used_exercises
    available = [e for e in EXERCISES if e["exercise"] not in used_exercises]
    if not available:
        used_exercises = []
        available = EXERCISES.copy()
    ex = random.choice(available)
    used_exercises.append(ex["exercise"])

    ans = simpledialog.askstring("Mini Exercise 🌱", ex["exercise"])
    if ans == ex["answer"]:
        messagebox.showinfo("Correct!", "🌿 Great job!")
    else:
        messagebox.showinfo("Incorrect", f"Correct answer: {ex['answer']}")

# Pomodoro variables
pomodoro_minutes = 25
pomodoro_seconds = 0
pomodoro_running = False
pomodoro_break = False

def update_timer_label():
    mins = str(pomodoro_minutes).zfill(2)
    secs = str(pomodoro_seconds).zfill(2)
    timer_label.config(text=f"{mins}:{secs}")

    total = 25*60 if not pomodoro_break else 5*60
    remaining = pomodoro_minutes*60 + pomodoro_seconds
    elapsed = total - remaining
    if total > 0:
        progress_bar['value'] = int((elapsed/total)*100)
    else:
        progress_bar['value'] = 0

def start_pomodoro():
    global pomodoro_running, pomodoro_minutes, pomodoro_seconds, pomodoro_break
    if pomodoro_running:
        return
    pomodoro_running = True
    pomodoro_minutes = 25 if not pomodoro_break else 5
    pomodoro_seconds = 0
    status_label.config(text="Pomodoro running" if not pomodoro_break else "Break running")
    update_timer_label()
    countdown()

def stop_pomodoro():
    global pomodoro_running
    pomodoro_running = False
    status_label.config(text="Pomodoro stopped")

def countdown():
    global pomodoro_minutes, pomodoro_seconds, pomodoro_running, pomodoro_break
    if pomodoro_running:
        if pomodoro_seconds == 0:
            if pomodoro_minutes == 0:
                pomodoro_running = False
                if not pomodoro_break:
                    messagebox.showinfo("Focus Done 🌿", "Take a 5-minute break.")
                    pomodoro_break = True
                else:
                    messagebox.showinfo("Break Done 🍃", "Let's focus again!")
                    pomodoro_break = False
                start_pomodoro()
                return
            else:
                pomodoro_minutes -= 1
                pomodoro_seconds = 59
        else:
            pomodoro_seconds -= 1
        update_timer_label()
        root.after(1000, countdown)

# -------------------------
# Task UI functions (DB-backed)
# -------------------------
def refresh_tasks():
    # Clear current widgets
    for widget in task_frame_inner.winfo_children():
        widget.destroy()

    try:
        rows = load_tasks_db()
    except Exception as e:
        # load_tasks_db already shows a messagebox on connection failure
        return

    for idx, r in enumerate(rows):
        bg = "#ecf4e8" if idx % 2 == 0 else "#f7fdf4"
        frame = tk.Frame(task_frame_inner, bg=bg, pady=5)
        frame.pack(fill="x")
        completed = bool(r.get("completed", 0))
        var = tk.BooleanVar(value=completed)
        display_text = f"#{r['id']}  {r['task']}  —  {r['deadline']}"
        cb = tk.Checkbutton(frame,
                            text=display_text,
                            variable=var,
                            bg=bg,
                            activebackground=bg,
                            font=("Segoe UI", 12, "overstrike" if completed else "normal"),
                            anchor="w",
                            command=lambda task_id=r['id'], v=var: toggle_task_db(task_id, v))
        cb.pack(fill="x", padx=10)

    # update scroll region
    try:
        task_canvas.configure(scrollregion=task_canvas.bbox("all"))
    except Exception:
        pass

def add_task():
    text = task_entry.get().strip()
    dl = deadline_entry.get().strip()
    if not text:
        messagebox.showwarning("Missing Input", "Task cannot be empty.")
        return
    try:
        save_task_db(text, dl or "No deadline")
    except Exception as e:
        # get_db_connection will show a messagebox; also show brief info
        messagebox.showerror("Error", f"Could not save task: {e}")
        return
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    refresh_tasks()

def toggle_task_db(task_id, var):
    try:
        update_task_completed_db(task_id, var.get())
    except Exception as e:
        messagebox.showerror("Error", f"Could not update task: {e}")
    refresh_tasks()

def delete_completed():
    try:
        delete_completed_db()
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete completed tasks: {e}")
    refresh_tasks()

# -------------------------
# Brain fog UI
# -------------------------
def brain_fog_detector():
    fog_window = tk.Toplevel(root)
    fog_window.title("Brain Fog Detector")
    fog_window.geometry("400x480")
    fog_window.config(bg="#e6fdff")

    title = tk.Label(fog_window, text="🧠 Brain Fog Detector", font=("Arial", 18, "bold"), bg="#e6f6ff")
    title.pack(pady=15)

    focus_var = tk.IntVar(value=3)
    sleepy_var = tk.IntVar(value=3)
    understand_var = tk.IntVar(value=3)
    memory_var = tk.IntVar(value=3)
    stress_var = tk.IntVar(value=3)

    def create_slider(text, variable):
        frame = tk.Frame(fog_window, bg="#e6feff")
        frame.pack(pady=8)
        tk.Label(frame, text=text, font=("Arial", 12), bg="#e6fbff").pack()
        tk.Scale(frame, from_=1, to=5, orient="horizontal", length=250, variable=variable, bg="#e6f2ff").pack()

    create_slider("Focus Level (1–5)", focus_var)
    create_slider("Sleepiness (1–5)", sleepy_var)
    create_slider("Understanding Speed (1–5)", understand_var)
    create_slider("Memory Sharpness (1–5)", memory_var)
    create_slider("Stress Level (1–5)", stress_var)

    def calculate_fog():
        f = focus_var.get()
        s = sleepy_var.get()
        u = understand_var.get()
        m = memory_var.get()
        st = stress_var.get()

        score = (f + u + m) - (s + st)
        if score >= 8:
            fog = "Clear Mind"
            tip = "Great day to study deeply!"
        elif score >= 3:
            fog = "Mild Fog"
            tip = "Take a 10-minute break and hydrate."
        else:
            fog = "Heavy Fog"
            tip = "Take a rest before studying."

        today_str = datetime.today().strftime("%Y-%m-%d")
        try:
            save_brain_fog_db(today_str, f, s, u, m, st, score, fog)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save brain fog entry: {e}")
            return

        messagebox.showinfo(fog, tip)
        fog_window.destroy()

    tk.Button(fog_window, text="Calculate", command=calculate_fog, font=("Arial", 14)).pack(pady=20)

# -------------------------
# GUI
# -------------------------
root = tk.Tk()
root.title("Study Buddy — Forest Edition (MySQL)")
root.geometry("1100x630")
root.config(bg="#dce9d5")

# Header
tk.Label(root, text="Study Buddy",
         font=("Segoe UI", 28, "bold"),
         bg="#c8dfc0").pack(fill="x", pady=10)

main_frame = tk.Frame(root, bg="#dce9d5")
main_frame.pack(fill="both", expand=True)

# LEFT: Task List
task_frame = tk.Frame(main_frame, bg="#cfe7c9", bd=3, relief="ridge")
task_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

task_canvas = tk.Canvas(task_frame, bg="#f7fdf4", highlightthickness=0)
scrollbar = tk.Scrollbar(task_frame, orient="vertical", command=task_canvas.yview)
task_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
task_canvas.pack(side="left", fill="both", expand=True)

task_frame_inner = tk.Frame(task_canvas, bg="#f7fdf4")
task_canvas.create_window((0, 0), window=task_frame_inner, anchor="nw")
task_frame_inner.bind("<Configure>", lambda e: task_canvas.configure(scrollregion=task_canvas.bbox("all")))

# RIGHT: Controls
control_frame = tk.Frame(main_frame, bg="#cfe7c9", bd=3, relief="ridge")
control_frame.pack(side="right", fill="y", padx=20, pady=20)

def forest_button(text, cmd):
    return tk.Button(control_frame, text=text, font=("Segoe UI", 12),
                     bg="#4d7c4a", fg="white", width=20, height=1,
                     relief="raised", bd=3, command=cmd)

tk.Label(control_frame, text="Task:", font=("Segoe UI", 12), bg="#cfe7c9").pack(pady=(10,0))
task_entry = tk.Entry(control_frame, font=("Segoe UI", 12), width=23)
task_entry.pack(pady=5)

tk.Label(control_frame, text="Deadline:", font=("Segoe UI", 12), bg="#cfe7c9").pack()
deadline_entry = tk.Entry(control_frame, font=("Segoe UI", 12), width=23)
deadline_entry.pack(pady=5)

forest_button("Add Task", add_task).pack(pady=5)
forest_button("Delete Completed", delete_completed).pack(pady=5)
forest_button("Motivation", motivate).pack(pady=5)
forest_button("Mini Exercise", mini_exercise).pack(pady=5)
forest_button("Start Pomodoro", start_pomodoro).pack(pady=5)
forest_button("Stop Pomodoro", stop_pomodoro).pack(pady=5)
forest_button("Brain Fog Detector", brain_fog_detector).pack(pady=5)

# Pomodoro display
timer_label = tk.Label(root, text="25:00", font=("Segoe UI", 48), bg="#dce9d5")
timer_label.pack()
status_label = tk.Label(root, text="Pomodoro not started", font=("Segoe UI", 16), bg="#dce9d5")
status_label.pack(pady=5)
progress_bar = ttk.Progressbar(root, length=250, mode="determinate", maximum=100)
progress_bar.pack(pady=10)

# Initialize DB and load tasks
try:
    init_db()
except Exception as e:
    # init_db shows a messagebox if connection fails; still continue to show GUI so user can see message.
    print("DB init error:", e)

refresh_tasks()
root.mainloop()
