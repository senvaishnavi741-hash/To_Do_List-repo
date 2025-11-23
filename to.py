import tkinter as tk
from tkinter import messagebox, ttk

# -----------------------------
# BACKEND TASK LIST
# -----------------------------
to_do_list = []

# ADD TASK
def add_task():
    task = entry_task.get().strip()
    if task:
        to_do_list.append({"Task": task, "Status": "Pending"})
        update_listbox()
        entry_task.delete(0, tk.END)
        messagebox.showinfo("Success", "Task Added Successfully!")
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

# UPDATE LISTBOX
def update_listbox():
    listbox_tasks.delete(*listbox_tasks.get_children())
    for i, t in enumerate(to_do_list, 1):
        listbox_tasks.insert("", "end", values=(i, t["Task"], t["Status"]))

# REMOVE TASK
def remove_task():
    selected = listbox_tasks.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a task to remove.")
        return

    index = listbox_tasks.index(selected[0])
    removed_task = to_do_list.pop(index)
    update_listbox()
    messagebox.showinfo("Removed", f"Task removed: {removed_task['Task']}")

# MARK TASK DONE
def mark_done():
    selected = listbox_tasks.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a task to mark as done.")
        return

    index = listbox_tasks.index(selected[0])
    to_do_list[index]["Status"] = "Done"
    update_listbox()
    messagebox.showinfo("Updated", "Task marked as done.")

# -----------------------------
# GUI WINDOW
# -----------------------------
root = tk.Tk()
root.title("To-Do List App")
root.geometry("500x450")
root.configure(bg="#e3f2fd")

# HEADING
title_label = tk.Label(root, text="To-Do List", font=("Arial", 20, "bold"), bg="#e3f2fd")
title_label.pack(pady=10)

# INPUT FIELD
frame_input = tk.Frame(root, bg="#e3ecfd")
frame_input.pack(pady=10)

entry_task = tk.Entry(frame_input, font=("Arial", 14), width=25)
entry_task.grid(row=0, column=0, padx=5)

btn_add = tk.Button(frame_input, text="Add Task", font=("Arial", 12), bg="#64b5f6", fg="white", activebackground="#42a5f5", command=add_task)
btn_add.grid(row=0, column=1, padx=5)

# TASK LIST TABLE
columns = ("Task No.", "Task", "Status")
listbox_tasks = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    listbox_tasks.heading(col, text=col)
    listbox_tasks.column(col, anchor="center", width=150)

listbox_tasks.pack(pady=10)

# BUTTONS FRAME
frame_btn = tk.Frame(root, bg="#e3f2fd")
frame_btn.pack(pady=10)

btn_remove = tk.Button(frame_btn, text="Remove Task", font=("Arial", 12), bg="#64b5f6", fg="white", activebackground="#42a5f5", command=remove_task)
btn_remove.grid(row=0, column=0, padx=10)

btn_done = tk.Button(frame_btn, text="Mark Done", font=("Arial", 12), bg="#64b5f6", fg="white", activebackground="#42a5f5", command=mark_done)
btn_done.grid(row=0, column=1, padx=10)

# RUN APP
root.mainloop()
