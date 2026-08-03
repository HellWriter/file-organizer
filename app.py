import os
import shutil
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".html", ".css", ".js", ".json", ".cpp", ".java"],
    "Executables": [".exe", ".msi", ".dmg", ".pkg"],
}

class FileOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto File Organizer")
        self.geometry("650x550")
        self.resizable(False, False)

        self.source_path = ctk.StringVar()
        self.dest_path = ctk.StringVar()
        self.sort_var = ctk.StringVar(value="format")
        self.action_var = ctk.StringVar(value="move")

        self._build_ui()

    def _build_ui(self):
        title_label = ctk.CTkLabel(self, text="Auto File Organizer", font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(pady=(15, 10))

        folder_frame = ctk.CTkFrame(self)
        folder_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(folder_frame, text="Source Folder:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.source_entry = ctk.CTkEntry(folder_frame, textvariable=self.source_path, width=350, placeholder_text="Select folder to clean up...")
        self.source_entry.grid(row=0, column=1, padx=5, pady=8)
        ctk.CTkButton(folder_frame, text="Browse", width=80, command=self.browse_source).grid(row=0, column=2, padx=10, pady=8)

        ctk.CTkLabel(folder_frame, text="Destination:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.dest_entry = ctk.CTkEntry(folder_frame, textvariable=self.dest_path, width=350, placeholder_text="Defaults to Source Folder if empty")
        self.dest_entry.grid(row=1, column=1, padx=5, pady=8)
        ctk.CTkButton(folder_frame, text="Browse", width=80, command=self.browse_dest).grid(row=1, column=2, padx=10, pady=8)

        options_frame = ctk.CTkFrame(self)
        options_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkLabel(options_frame, text="Organize By:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkRadioButton(options_frame, text="Format (Images, Documents)", variable=self.sort_var, value="format").grid(row=0, column=1, padx=10, sticky="w")
        ctk.CTkRadioButton(options_frame, text="Exact Extension (JPG, PDF)", variable=self.sort_var, value="extension").grid(row=0, column=2, padx=10, sticky="w")

        ctk.CTkLabel(options_frame, text="Transfer Method:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkRadioButton(options_frame, text="Move (Cut)", variable=self.action_var, value="move").grid(row=1, column=1, padx=10, sticky="w")
        ctk.CTkRadioButton(options_frame, text="Copy (Keep Original)", variable=self.action_var, value="copy").grid(row=1, column=2, padx=10, sticky="w")

        self.organize_btn = ctk.CTkButton(self, text="Organize Files", font=ctk.CTkFont(size=15, weight="bold"), height=40, command=self.run_organization)
        self.organize_btn.pack(padx=20, pady=10, fill="x")

        log_frame = ctk.CTkFrame(self)
        log_frame.pack(padx=20, pady=(0, 15), fill="both", expand=True)

        ctk.CTkLabel(log_frame, text="Activity Log:").pack(anchor="w", padx=10, pady=(5, 0))
        self.log_box = ctk.CTkTextbox(log_frame, state="disabled")
        self.log_box.pack(padx=10, pady=5, fill="both", expand=True)

    def browse_source(self):
        if folder := filedialog.askdirectory(title="Select Source Folder"):
            self.source_path.set(folder)

    def browse_dest(self):
        if folder := filedialog.askdirectory(title="Select Destination Folder"):
            self.dest_path.set(folder)

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def run_organization(self):
        src = self.source_path.get().strip()
        dest = self.dest_path.get().strip() or src

        if not src or not Path(src).exists():
            messagebox.showerror("Error", "Please select a valid Source Folder.")
            return

        source_dir = Path(src)
        dest_dir = Path(dest)
        action_mode = self.action_var.get()
        sort_mode = self.sort_var.get()

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

        action_text = "Moving" if action_mode == "move" else "Copying"
        self.log(f"Starting file transfer ({action_text})...\nFrom: {source_dir}\nTo:   {dest_dir}\n" + "-"*45)

        processed_count = 0

        try:
            for item in source_dir.iterdir():
                if item.is_dir():
                    continue

                file_ext = item.suffix.lower()
                if not file_ext:
                    continue

                folder_name = "Others"

                if sort_mode == "format":
                    for category, extensions in FILE_CATEGORIES.items():
                        if file_ext in extensions:
                            folder_name = category
                            break
                else:
                    folder_name = file_ext.replace(".", "").upper()

                target_folder = dest_dir / folder_name
                target_folder.mkdir(parents=True, exist_ok=True)
                
                if action_mode == "move":
                    shutil.move(str(item), str(target_folder / item.name))
                    self.log(f"[Moved] {item.name} -> {folder_name}/")
                else:
                    shutil.copy2(str(item), str(target_folder / item.name))
                    self.log(f"[Copied] {item.name} -> {folder_name}/")
                    
                processed_count += 1

            self.log("-" * 45)
            self.log(f"Process Complete! Total files processed: {processed_count}")
            messagebox.showinfo("Success", f"Successfully {action_text.lower()} {processed_count} file(s).")

        except Exception as e:
            self.log(f"\n[ERROR] {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()