import os
import tkinter as tk
from tkinter import ttk

class VideoCourseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Course Tracker")
        
        self.tree = ttk.Treeview(self.root, columns=("Video", "Progress"))
        self.tree.heading("#0", text="Course Folder", anchor="w")
        self.tree.heading("Video", text="Video")
        self.tree.heading("Progress", text="Progress")
        self.tree.column("#0", stretch=tk.YES)
        self.tree.column("Video", anchor="center", width=200)
        self.tree.column("Progress", anchor="center", width=100)
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.load_course_data()
        
    def load_course_data(self):
        course_folder = "C:\Diploma\Power BI"
        if os.path.exists(course_folder):
            videos = [video for video in os.listdir(course_folder) if video.endswith(('.mp4', '.avi', '.mkv'))]
            for video in videos:
                self.tree.insert("", "end", values=(video, "Not Watched"))
                
    def mark_as_watched(self):
        selected_item = self.tree.selection()
        if selected_item:
            progress = "Watched"
            self.tree.item(selected_item, values=(self.tree.item(selected_item, "values")[0], progress))
            self.update_course_progress()

    def update_course_progress(self):
        watched_videos = [item for item in self.tree.get_children() if self.tree.item(item, "values")[1] == "Watched"]
        total_videos = self.tree.get_children()
        course_progress = f"{len(watched_videos)}/{len(total_videos)} videos watched"
        self.root.title(f"Video Course Tracker - {course_progress}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCourseTracker(root)
    
    mark_button = tk.Button(root, text="Mark as Watched", command=app.mark_as_watched)
    mark_button.pack(pady=10)
    
    root.mainloop()
