import os
import shutil
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ExtensionOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto File Organizer")
        self.geometry("650x600")
        self.resizable(False, False)

        self.source_path = ctk.StringVar()
        self.dest_path = ctk.StringVar()
        self.clean_all_var = ctk.BooleanVar(value=True)
        self.action_var = ctk.StringVar(value="move")

        self._build_ui()

    def _build_ui(self):
        title_label = ctk.CTkLabel(self, text="Sort Files by Exact Extension", font=ctk.CTkFont(size=22, weight="bold"))
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

        ext_frame = ctk.CTkFrame(self)
        ext_frame.pack(padx=20, pady=10, fill="x")

        self.clean_all_cb = ctk.CTkCheckBox(
            ext_frame, 
            text="Clean Whole Folder (All Extensions)", 
            variable=self.clean_all_var, 
            command=self.toggle_ext_entry,
            font=ctk.CTkFont(weight="bold")
        )
        self.clean_all_cb.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        ctk.CTkLabel(ext_frame, text="Or target specific extensions (comma separated):").grid(row=1, column=0, padx=10, pady=(5, 10), sticky="w")
        self.ext_entry = ctk.CTkEntry(ext_frame, width=250, placeholder_text="e.g. jpg, pdf, mp4", state="disabled")
        self.ext_entry.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="w")

        action_frame = ctk.CTkFrame(self)
        action_frame.pack(padx=20, pady=(0, 10), fill="x")
        
        ctk.CTkLabel(action_frame, text="Transfer Method:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10)
        ctk.CTkRadioButton(action_frame, text="Move (Cut)", variable=self.action_var, value="move").pack(side="left", padx=15)
        ctk.CTkRadioButton(action_frame, text="Copy (Keep Original)", variable=self.action_var, value="copy").pack(side="left", padx=15)

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

    def toggle_ext_entry(self):
        state = "disabled" if self.clean_all_var.get() else "normal"
        self.ext_entry.configure(state=state)

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
        clean_all = self.clean_all_var.get()
        
        target_exts = []
        if not clean_all:
            raw_exts = self.ext_entry.get().split(",")
            target_exts = [ext.strip().lower().replace(".", "") for ext in raw_exts if ext.strip()]
            
            if not target_exts:
                messagebox.showwarning("Warning", "Enter at least one extension or select 'Clean Whole Folder'.")
                return

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

                file_ext = item.suffix.lower().replace(".", "")
                if not file_ext:
                    continue

                if clean_all or file_ext in target_exts:
                    folder_name = file_ext.upper()
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
    app = ExtensionOrganizerApp()
    app.mainloop()