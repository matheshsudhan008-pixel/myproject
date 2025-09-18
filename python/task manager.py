import tkinter as tk
from tkinter import messagebox
import os

FILENAME = "tasks.txt"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x500")
        self.root.configure(bg="#222")

        self.tasks = []

        # Entry field
        self.task_input = tk.Entry(root, font=("Arial", 14), bd=0, bg="#333", fg="white")
        self.task_input.pack(pady=10, padx=10, fill="x")

        # Buttons
        button_frame = tk.Frame(root, bg="#222")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Add Task", command=self.add_task, bg="#2ecc71", fg="white", bd=0, width=10).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task, bg="#e74c3c", fg="white", bd=0, width=10).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Mark Done", command=self.mark_done, bg="#f39c12", fg="white", bd=0, width=10).grid(row=0, column=2, padx=5)

        # Task listbox
        self.listbox = tk.Listbox(root, font=("Arial", 14), selectmode=tk.SINGLE, bg="#333", fg="white", selectbackground="#2ecc71")
        self.listbox.pack(pady=10, padx=10, fill="both", expand=True)

        # Load tasks if available
        self.load_tasks()

    def add_task(self):
        task = self.task_input.get().strip()
        if task:
            self.listbox.insert(tk.END, task)
            self.tasks.append(task)
            self.task_input.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a task!")

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            self.tasks.pop(index)
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")

    def mark_done(self):
        try:
            index = self.listbox.curselection()[0]
            task = self.tasks[index]
            if not task.startswith("✔ "):
                self.tasks[index] = "✔ " + task
                self.listbox.delete(index)
                self.listbox.insert(index, "✔ " + task)
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark done!")

    def save_tasks(self):
        with open(FILENAME, "w") as f:
            for task in self.tasks:
                f.write(task + "\n")

    def load_tasks(self):
        if os.path.exists(FILENAME):
            with open(FILENAME, "r") as f:
                self.tasks = [line.strip() for line in f.readlines()]
            for task in self.tasks:
                self.listbox.insert(tk.END, task)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
