#!/usr/bin/env python3
"""
Zip-to-APK Renamer (Simple GUI)

What it does:
- Lets a user pick one or more .zip files
- Renames them to .apk in-place (no copying)

How to run:
  python3 zip_to_apk.py

Notes:
- Uses the built-in tkinter module (no extra dependencies)
- If a destination file already exists, appends a numeric suffix
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path


def rename_zip_to_apk(file_paths):
    """Rename a list of .zip files to .apk, returning (successes, failures)."""
    successes = []
    failures = []

    for file_path in file_paths:
        try:
            src = Path(file_path)
            if not src.exists():
                failures.append((file_path, "File not found"))
                continue

            if src.suffix.lower() != ".zip":
                failures.append((file_path, "Not a .zip file"))
                continue

            base = src.with_suffix("")
            dst = base.with_suffix(".apk")

            # If destination exists, add a numeric suffix
            counter = 1
            while dst.exists():
                dst = base.with_name(f"{base.name}({counter})").with_suffix(".apk")
                counter += 1

            os.rename(src, dst)
            successes.append((str(src), str(dst)))
        except Exception as exc:
            failures.append((file_path, str(exc)))

    return successes, failures


def pick_and_rename():
    file_paths = filedialog.askopenfilenames(
        title="Select .zip files to rename to .apk",
        filetypes=[("ZIP files", "*.zip")]
    )
    if not file_paths:
        return

    successes, failures = rename_zip_to_apk(file_paths)

    # Compose a simple report
    lines = []
    if successes:
        lines.append("Renamed:")
        for src, dst in successes:
            lines.append(f"  ✓ {Path(src).name} -> {Path(dst).name}")
    if failures:
        if lines:
            lines.append("")
        lines.append("Skipped/Failed:")
        for fp, reason in failures:
            lines.append(f"  ✗ {Path(fp).name} — {reason}")

    if not lines:
        lines = ["No files processed."]

    messagebox.showinfo("Zip-to-APK", "\n".join(lines))


def main():
    root = tk.Tk()
    root.title("CircleFlight")
    root.resizable(False, False)

    # Hide the main window (we only need the dialog), but keep a tiny UI for clarity
    frame = tk.Frame(root, padx=16, pady=16)
    frame.pack()

    label = tk.Label(frame, text="Select .zip files to rename to .apk")
    label.pack(anchor="w", pady=(0, 8))

    pick_btn = tk.Button(frame, text="Choose .zip files…", command=pick_and_rename, width=24)
    pick_btn.pack(pady=(0, 8))

    quit_btn = tk.Button(frame, text="Close", command=root.destroy, width=24)
    quit_btn.pack()

    # Center the small window
    root.update_idletasks()
    w, h = 320, 160
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
