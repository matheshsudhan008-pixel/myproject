import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

FILENAME = "tasks.txt"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 To-Do List")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e1e1e")

        self.tasks = self.load_tasks()

        # Title
        title = tk.Label(root, text="My Tasks ✅", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="#f1c40f")
        title.pack(pady=10)

        # Input field
        self.task_input = tk.Entry(root, font=("Arial", 14), bd=0, bg="#2c2c2c", fg="white", insertbackground="white")
        self.task_input.pack(pady=10, padx=20, fill="x")
        self.task_input.bind("<Return>", lambda e: self.add_task())  # Press Enter to add task

        # Buttons
        button_frame = tk.Frame(root, bg="#1e1e1e")
        button_frame.pack(pady=5)

        self.make_button(button_frame, "➕ Add", self.add_task, "#27ae60", 0)
        self.make_button(button_frame, "❌ Delete", self.delete_task, "#e74c3c", 1)
        self.make_button(button_frame, "✔ Toggle Done", self.mark_done, "#f39c12", 2)

        # Scrollable Listbox
        list_frame = tk.Frame(root, bg="#1e1e1e")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.listbox = tk.Listbox(
            list_frame, font=("Arial", 14), selectmode=tk.SINGLE,
            bg="#2c2c2c", fg="white", selectbackground="#27ae60",
            activestyle="none", highlightthickness=0, relief="flat"
        )

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind keyboard shortcuts
        self.listbox.bind("<Delete>", lambda e: self.delete_task())
        self.listbox.bind("<space>", lambda e: self.mark_done())

        # Task count
        self.task_count = tk.Label(root, text="", font=("Arial", 12), bg="#1e1e1e", fg="gray")
        self.task_count.pack(pady=5)

        self.refresh_listbox()

    def make_button(self, parent, text, command, color, col):
        btn = tk.Button(
            parent, text=text, command=command, bg=color, fg="white",
            font=("Arial", 12, "bold"), relief="flat", bd=0, padx=10, pady=8
        )
        btn.grid(row=0, column=col, padx=5, ipadx=5, sticky="nsew")
        btn.bind("<Enter>", lambda e: btn.config(bg=self.darken(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

    def darken(self, color):
        """Darken a HEX color slightly for hover effect"""
        color = color.lstrip("#")
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, int(c * 0.85)) for c in rgb)
        return "#%02x%02x%02x" % rgb

    def add_task(self):
        task = self.task_input.get().strip()
        if task:
            self.tasks.append(task)
            self.refresh_listbox()
            self.task_input.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a task!")

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            del self.tasks[index]
            self.refresh_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")

    def mark_done(self):
        try:
            index = self.listbox.curselection()[0]
            if self.tasks[index].startswith("✔ "):
                self.tasks[index] = self.tasks[index][2:]  # remove checkmark
            else:
                self.tasks[index] = "✔ " + self.tasks[index]
            self.refresh_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark done!")

    def save_tasks(self):
        try:
            with open(FILENAME, "w") as f:
                for task in self.tasks:
                    f.write(task + "\n")
        except OSError as e:
            messagebox.showerror("File Error", f"Error saving tasks: {e}")

    def load_tasks(self):
        tasks = []
        try:
            if os.path.exists(FILENAME):
                with open(FILENAME, "r") as f:
                    tasks = [line.strip() for line in f.readlines()]
        except OSError as e:
            messagebox.showerror("File Error", f"Error loading tasks: {e}")
        return tasks

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)
        self.task_count.config(text=f"Total Tasks: {len(self.tasks)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
