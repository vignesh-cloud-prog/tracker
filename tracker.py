"""
Video Course Tracker
Developed by Vignesh_N_U
For support and contact, call 7338085595 or email vigneshun80@gmail.com
Copyright (c) 2024 Vignesh_N_U
"""

import os
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class VideoCourseTracker:
    import tkinter.messagebox as messagebox

    def __init__(self, root, courses_path):
        self.root = root
        self.root.title("Video Course Tracker")
        
        self.tree = ttk.Treeview(self.root, columns=("Progress",), show="tree")
        self.tree.heading("#0", text="Course Folder", anchor="w")
        self.tree.heading("Progress", text="Progress")
        self.tree.column("#0", stretch=tk.YES, width=300)
        self.tree.column("Progress", anchor="center", width=100)
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.courses_path = os.path.abspath(courses_path)
        self.db_file = os.path.abspath("videoprogress.db")
        self.create_db_table()

        self.load_course_data()
        self.create_context_menu()
        copyright_label = tk.Label(root, text="Copyright (c) 2024 Vignesh_N_U\nDeveloped with 💝 for HIS\nFor support and contact, call 7338085595 or email vigneshun80@gmail.com")
        copyright_label.pack(pady=10)

        # Add a menu option to reset all progress
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        reset_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=reset_menu)
        reset_menu.add_command(label="Reset All Progress", command=self.reset_all_progress)

    def reset_all_progress(self):
        # Display a confirmation dialog
        confirm = messagebox.askyesno("Reset All Progress", "Are you sure you want to reset all progress? This action cannot be undone.")

        if confirm:
            # Clear all data from the database
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("DELETE FROM video_progress")
            conn.commit()
            conn.close()

            # Clear the treeview
            self.tree.delete(*self.tree.get_children())

            # Reload the course data
            self.load_course_data()
            messagebox.showinfo("Reset All Progress", "All progress has been reset.")

    def create_db_table(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS video_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_path TEXT,
                video_name TEXT,
                progress TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def load_course_data(self, parent="", folder_path=None):
        if folder_path is None:
            folder_path = self.courses_path

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                folder_id = self.tree.insert(parent, "end", text=item, values=(self.get_folder_progress(item_path),))
                self.load_course_data(parent=folder_id, folder_path=item_path)
            elif item.endswith(('.mp4', '.avi', '.mkv')):
                video_path = os.path.join(folder_path, item)
                progress = self.get_video_progress(video_path)
                self.tree.insert(parent, "end", text=item, values=(progress,))

        conn.close()
        self.update_course_progress()

    def create_context_menu(self):
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Mark as Watched", command=self.mark_as_watched)
        context_menu.add_command(label="Mark as Completed", command=self.mark_as_completed)
        context_menu.add_command(label="Mark as Not Watched", command=self.mark_as_not_watched)

        def show_context_menu(event):
            item = self.tree.identify_row(event.y)
            if item:
                context_menu.post(event.x_root, event.y_root)

        self.tree.bind("<Button-3>", show_context_menu)

    def mark_as_watched(self):
        selected_item = self.tree.selection()
        if selected_item:
            progress = "Watched"
            item_path = self.get_item_path(selected_item)
            self.tree.item(selected_item, values=(progress,))
            self.update_database(item_path, progress)
            self.update_course_progress()

    def mark_as_completed(self):
        selected_item = self.tree.selection()
        if selected_item:
            progress = "Completed"
            item_path = self.get_item_path(selected_item)
            self.tree.item(selected_item, values=(progress,))
            self.update_database(item_path, progress)
            self.update_course_progress()

    def mark_as_not_watched(self):
        selected_item = self.tree.selection()
        if selected_item:
            progress = "Not Watched"
            item_path = self.get_item_path(selected_item)
            self.tree.item(selected_item, values=(progress,))
            self.update_database(item_path, progress)
            self.update_course_progress()

    def update_database(self, item_path, progress):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        video_name = None  # Set video_name to None for null value
        if os.path.isdir(item_path):
            c.execute("SELECT * FROM video_progress WHERE folder_path=? AND video_name IS NULL", (item_path,))
            result = c.fetchone()
            if result:
                c.execute("UPDATE video_progress SET progress=? WHERE folder_path=? AND video_name IS NULL", (progress, item_path))
            else:
                c.execute("INSERT INTO video_progress (folder_path, progress) VALUES (?, ?)", (item_path, progress))
        else:
            folder_path, video_name = os.path.split(item_path)
            c.execute("SELECT * FROM video_progress WHERE folder_path=? AND video_name=?", (folder_path, video_name))
            result = c.fetchone()
            if result:
                c.execute("UPDATE video_progress SET progress=? WHERE folder_path=? AND video_name=?", (progress, folder_path, video_name))
            else:
                c.execute("INSERT INTO video_progress (folder_path, video_name, progress) VALUES (?, ?, ?)", (folder_path, video_name, progress))

        conn.commit()
        conn.close()

    def get_folder_progress(self, folder_path):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        video_name = None  # Set video_name to None for null value
        c.execute("SELECT progress FROM video_progress WHERE folder_path=? AND video_name IS ?", (folder_path, video_name))
        result = c.fetchone()

        conn.close()

        return result[0] if result else "Not Watched"

    def get_video_progress(self, video_path):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        folder_path, video_name = os.path.split(video_path)
        c.execute("SELECT progress FROM video_progress WHERE folder_path=? AND video_name=?", (folder_path, video_name))
        result = c.fetchone()

        conn.close()

        return result[0] if result else "Not Watched"


    def get_item_path(self, item):
        item_path = self.tree.item(item, "text")
        parent = self.tree.parent(item)
        while parent:
            item_path = os.path.join(self.tree.item(parent, "text"), item_path)
            parent = self.tree.parent(parent)

        return os.path.join(self.courses_path, item_path)

    def update_course_progress(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        watched_videos = [item for item in self.tree.get_children() if self.tree.item(item, "values")[0] == "Completed"]
        total_videos = self.tree.get_children()
        

        course_progress = f"{len(watched_videos)}/{len(total_videos)} completed"
        self.root.title(f"Video Course Tracker - {course_progress}")

        conn.close()

if __name__ == "__main__":
    folder_path = filedialog.askdirectory(title="Select Course Folder")
    if folder_path:
        root = tk.Tk()
        app = VideoCourseTracker(root, folder_path)
        root.focus_force()
        root.mainloop()
