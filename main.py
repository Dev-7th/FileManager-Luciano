import tkinter as tk
from tkinter import messagebox
import os

# Your custom modules
import analyzer
import rules
import mover
import undeor
from gui import FileOrganizerGUI


class Controller:
    def __init__(self):
        self.root = tk.Tk()
        # Initialize GUI and pass the functions (callbacks) it should run
        self.gui = FileOrganizerGUI(
            self.root,
            analyze_cmd=self.handle_analyze,
            organize_cmd=self.handle_organize,
            move_cmd=self.handle_move,
            undo_cmd=self.handle_undo
        )
        self.processed_list = []

    def handle_analyze(self):
        path = self.gui.path_entry.get()
        if os.path.exists(path):
            files = os.listdir(path)
            self.processed_list = analyzer.file_analyzer(path, files)
            # Update the first tree
            self.gui.update_tree(self.gui.tree, self.processed_list, [
                                 "FileName", "Name", "Extension", "Date"])
            self.gui.show_frame("result")
        else:
            messagebox.showerror("Error", "That folder path does not exist!")

    def handle_organize(self):
        # Apply rules to our current list
        self.processed_list = rules.file_rules(self.processed_list)
        # Update the suggestion tree
        self.gui.update_tree(self.gui.suggest_tree, self.processed_list, [
                             "FileName", "category"])
        self.gui.show_frame("category")

    def handle_move(self):
        path = self.gui.path_entry.get()
        # Run the mover logic
        summary = mover.mover_func(path, self.processed_list)
        # Update the final log
        self.gui.display_log(summary)
        self.gui.show_frame("final")

    def handle_undo(self, filename):
        full_log_path = os.path.join("history-log", filename)
        # Run the logic from your undeor.py
        undo_summary = undeor.undeor(full_log_path)

        # Tell GUI to show the result on the new screen
        self.gui.display_undo_log(undo_summary)
        self.gui.show_frame("undo_screen")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Controller()
    app.run()
