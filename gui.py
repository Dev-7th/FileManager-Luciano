import tkinter as tk
from tkinter import ttk, filedialog
import os  # Needed to list the files in the folder


class FileOrganizerGUI:
    # undo_cmd will now be the function that handles the ACTUAL moving back of files
    def __init__(self, root, analyze_cmd, organize_cmd, move_cmd, undo_cmd):
        self.root = root
        self.root.title("File Organizer v1.0")
        self.root.geometry("1000x550")  # Slightly taller for the listbox

        self.undo_executor = undo_cmd  # Save the undo logic for later
        self.frames = {}

        # 1. Welcome Screen
        self.frames["welcome"] = tk.Frame(root, bg="#34495e")
        tk.Label(self.frames["welcome"], text="Welcome to File Organizer",
                 fg="white", bg="#34495e", font=("Arial", 18)).pack(pady=50)
        tk.Button(self.frames["welcome"], text="START", command=lambda: self.show_frame(
            "input"), width=10, height=2, bg="#2ecc71", fg="white", font=("Arial", 12, "bold")).pack()

        # 2. Input Screen (UPDATED: Added Undo Button)
        self.frames["input"] = tk.Frame(root, bg="#ecf0f1")
        tk.Label(self.frames["input"], text="Select the folder you want to organize:",
                 bg="#ecf0f1", font=("Arial", 12)).pack(pady=(40, 10))

        entry_frame = tk.Frame(self.frames["input"], bg="#ecf0f1")
        entry_frame.pack(pady=10)
        self.path_entry = tk.Entry(entry_frame, width=50, font=("Arial", 12))
        self.path_entry.pack(side="left", padx=5)
        tk.Button(entry_frame, text="Browse...", command=self.browse_folder,
                  bg="#95a5a6", fg="white").pack(side="left")

        tk.Button(self.frames["input"], text="Analyze Folder", command=analyze_cmd,
                  bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=20).pack(pady=10)

        # New Undo Button on Input Screen
        tk.Button(self.frames["input"], text="GO TO HISTORY / UNDO",
                  command=lambda: self.show_history_frame(),
                  bg="#e67e22", fg="white", font=("Arial", 10)).pack(pady=5)

        # 3. Result Screen
        self.frames["result"] = tk.Frame(root, bg="#ecf0f1")
        self.tree = ttk.Treeview(self.frames["result"], columns=(
            "filename", "name", "ext", "date"), show="headings")
        for col in ["filename", "name", "ext", "date"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Button(self.frames["result"], text="BACK", command=lambda: self.show_frame(
            "input"), bg="#3498db", fg="white").pack(side="left", padx=20, pady=20)
        tk.Button(self.frames["result"], text="ORGANIZED", command=organize_cmd,
                  bg="#3498db", fg="white").pack(side="right", padx=20, pady=20)

        # 4. Category Suggestion Screen
        self.frames["category"] = tk.Frame(root, bg="#ecf0f1")
        self.suggest_tree = ttk.Treeview(self.frames["category"], columns=(
            "filename", "category"), show="headings")
        self.suggest_tree.heading("filename", text="File Name")
        self.suggest_tree.heading("category", text="Category")
        self.suggest_tree.pack(pady=20, padx=20, fill="both", expand=True)
        tk.Button(self.frames["category"], text="MOVE",
                  command=move_cmd, bg="#3498db", fg="white").pack(pady=20)

        # 5. Final Log Screen (UPDATED: Undo button goes to History Frame)
        self.frames["final"] = tk.Frame(root, bg="#ecf0f1")
        tk.Label(self.frames["final"], text="Process Summary",
                 font=("Arial", 14, "bold")).pack(pady=10)
        self.log_box = tk.Text(
            self.frames["final"], height=12, width=80, state='disabled', bg="#f0f0f0")
        self.log_box.pack(pady=10, padx=20)

        final_btn_frame = tk.Frame(self.frames["final"], bg="#ecf0f1")
        final_btn_frame.pack(pady=10)

        tk.Button(final_btn_frame, text="VIEW HISTORY / UNDO", command=lambda: self.show_history_frame(),
                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)
        tk.Button(final_btn_frame, text="FINISH", command=lambda: self.show_frame("welcome"),
                  bg="#2ecc71", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)

        # 6. NEW: History Selection Frame
        self.frames["history_selection"] = tk.Frame(root, bg="#2c3e50")
        tk.Label(self.frames["history_selection"], text="Select a History Log to Undo:",
                 fg="white", bg="#2c3e50", font=("Arial", 14, "bold")).pack(pady=20)

        # The Listbox to show files
        self.history_listbox = tk.Listbox(
            self.frames["history_selection"], width=70, height=10, font=("Courier", 10))
        self.history_listbox.pack(pady=10, padx=20)

        hist_btn_frame = tk.Frame(
            self.frames["history_selection"], bg="#2c3e50")
        hist_btn_frame.pack(pady=20)

        tk.Button(hist_btn_frame, text="BACK", command=lambda: self.show_frame("input"),
                  bg="#95a5a6", width=15).pack(side="left", padx=10)

        # This button will trigger the actual undo logic
        tk.Button(hist_btn_frame, text="SELECT & UNDO", command=self.on_undo_click,
                  bg="#e67e22", fg="white", width=15, font=("Arial", 10, "bold")).pack(side="left", padx=10)

        # 7. Undo Results Log Screen (Same as before)
        self.frames["undo_screen"] = tk.Frame(root, bg="#f39c12")
        tk.Label(self.frames["undo_screen"], text="Undo Operation Log",
                 fg="white", bg="#f39c12", font=("Arial", 14, "bold")).pack(pady=10)
        self.undo_log_box = tk.Text(
            self.frames["undo_screen"], height=15, width=80, state='disabled')
        self.undo_log_box.pack(pady=10, padx=20)
        tk.Button(self.frames["undo_screen"], text="BACK TO START",
                  command=lambda: self.show_frame("welcome"), bg="white").pack(pady=10)

        self.show_frame("welcome")

    # --- NEW METHODS ---

    def show_history_frame(self):
        """Refreshes the log list and switches to the history frame"""
        self.history_listbox.delete(0, tk.END)  # Clear old list

        log_dir = "history-log"
        if os.path.exists(log_dir):
            logs = [f for f in os.listdir(log_dir) if f.endswith(".json")]
            for log in sorted(logs, reverse=True):  # Newest logs first
                self.history_listbox.insert(tk.END, log)

        self.show_frame("history_selection")

    def on_undo_click(self):
        """Gets the selected filename and passes it to the controller"""
        selection = self.history_listbox.curselection()
        if selection:
            # Get the string text from the clicked row
            selected_file = self.history_listbox.get(selection[0])
            # Pass it back to the Controller (main.py)
            self.undo_executor(selected_file)
        else:
            tk.messagebox.showwarning(
                "Selection Required", "Please click on a log file first!")

    # --- EXISTING METHODS ---
    def browse_folder(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, selected_directory)

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)

    def update_tree(self, tree_widget, data, columns):
        for item in tree_widget.get_children():
            tree_widget.delete(item)
        for row in data:
            values = [row[col] for col in columns]
            tree_widget.insert("", "end", values=values)

    def display_log(self, text):
        self.log_box.config(state='normal')
        self.log_box.delete("1.0", tk.END)
        self.log_box.insert(tk.END, text)
        self.log_box.config(state='disabled')

    def display_undo_log(self, text):
        self.undo_log_box.config(state='normal')
        self.undo_log_box.delete("1.0", tk.END)
        self.undo_log_box.insert(tk.END, text)
        self.undo_log_box.config(state='disabled')
