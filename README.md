# Auto File Organizer

A sleek, Python-based desktop application built with `customtkinter` that automatically organizes cluttered folders. It scans a source folder and sorts files into specific subfolders based on their exact file extensions (e.g., moving all `.jpg` files into a `JPG` folder, `.pdf` files into a `PDF` folder).

## Features

- **Modern GUI**: Built with CustomTkinter for a clean, system-native dark/light mode appearance.
- **Sort by Exact Extension**: Dynamically creates folders named after the file extensions.
- **Specific Targeting**: Choose to clean the entire folder automatically, or input specific extensions to organize (e.g., `jpg, mp4, pdf`) while ignoring the rest.
- **Move vs. Copy**: Gives you the option to completely move (cut) files to the new location or just copy them to keep your originals intact.
- **Custom Destinations**: Organize files within the same folder, or select an entirely different drive/directory as the destination.
- **Live Activity Log**: Watch the transfer process in real-time directly within the app.

## Requirements

- Python 3.7 or higher
- `customtkinter`

## Installation

1. Clone or download this repository to your local machine.
2. Open a terminal or command prompt in the project folder.
3. Install the required dependency by running:
   ```bash
   pip install customtkinter