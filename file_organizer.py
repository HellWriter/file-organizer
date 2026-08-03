import os
import shutil
from pathlib import Path

TARGET_DIR = Path.home() / "Downloads"

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".html", ".css", ".js", ".json", ".cpp", ".java"],
    "Executables": [".exe", ".msi", ".dmg", ".pkg"],
}

def organize_folder(target_path):
    folder = Path(target_path)
    
    if not folder.exists():
        print(f"Directory not found: {folder}")
        return

    for item in folder.iterdir():
        if item.is_dir():
            continue

        file_ext = item.suffix.lower()
        moved = False

        for category, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                dest_dir = folder / category
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(item), str(dest_dir / item.name))
                print(f"Moved '{item.name}' -> '{category}'")
                moved = True
                break

        if not moved and file_ext != "":
            dest_dir = folder / "Others"
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_dir / item.name))
            print(f"Moved '{item.name}' -> 'Others'")

if __name__ == "__main__":
    organize_folder(TARGET_DIR)