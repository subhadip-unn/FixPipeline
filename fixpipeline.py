#!/usr/bin/env python3
"""
FixPipeline - Professional CircleCI APK Auto-Fixer
Automatically converts CircleCI APK downloads from .zip to .apk files.

Usage:
    fixpipeline                    # Start system tray app
    fixpipeline --gui              # Open manual GUI tool
    fixpipeline --help             # Show help
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import pystray
    from PIL import Image, ImageDraw
    import plyer
except ImportError:
    print("Installing required packages...")
    os.system("pip install pystray pillow plyer watchdog psutil")
    import pystray
    from PIL import Image, ImageDraw
    import plyer

# Configuration
CONFIG_FILE = Path.home() / '.fixpipeline_config.json'
DEFAULT_CONFIG = {
    'watch_dir': str(Path.home() / 'Downloads'),
    'notifications': True,
    'target_files': [
        'app-production-release.apk',
        'app-staging-release.apk', 
        'app-production-debug.apk',
        'app-staging-debug.apk'
    ]
}

class FixPipelineHandler(FileSystemEventHandler):
    """File system event handler for APK auto-fixing."""
    
    def __init__(self, config):
        self.config = config
        self.processed_files = set()
        self.is_paused = False
        
    def pause(self):
        self.is_paused = True
        
    def resume(self):
        self.is_paused = False
        
    def on_created(self, event):
        if self.is_paused or event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if file_path.suffix.lower() != '.zip':
            return
            
        # Wait for download to complete
        time.sleep(2)
        
        if not file_path.exists():
            return
            
        # Check if this matches our target files
        if self.is_target_apk(file_path):
            self.fix_apk_file(file_path)
            
    def is_target_apk(self, file_path):
        """Check if file matches our target APK patterns."""
        filename = file_path.name.lower()
        target_files = [f.lower() for f in self.config['target_files']]
        
        # Check exact matches or patterns
        for target in target_files:
            if target in filename or filename.replace('.zip', '') in target:
                return True
        return False
        
    def fix_apk_file(self, file_path):
        """Fix APK file by renaming .zip to .apk."""
        try:
            # Create new filename with .apk extension
            new_path = file_path.with_suffix('.apk')
            
            # Handle existing files
            counter = 1
            while new_path.exists():
                stem = file_path.stem
                new_path = file_path.parent / f"{stem}({counter}).apk"
                counter += 1
                
            # Rename the file
            file_path.rename(new_path)
            
            # Show notification
            if self.config.get('notifications', True):
                self.show_notification(
                    "FixPipeline - APK Fixed!",
                    f"Converted {file_path.name} to {new_path.name}"
                )
                
            print(f"✅ Fixed: {file_path.name} -> {new_path.name}")
            self.processed_files.add(str(new_path))
            
        except Exception as e:
            print(f"❌ Error fixing {file_path.name}: {e}")
            if self.config.get('notifications', True):
                self.show_notification(
                    "FixPipeline - Error",
                    f"Could not convert {file_path.name}: {str(e)}"
                )
                
    def show_notification(self, title, message):
        """Show system notification."""
        try:
            plyer.notification.notify(
                title=title,
                message=message,
                timeout=5
            )
        except Exception as e:
            print(f"Notification failed: {e}")

class FixPipelineTray:
    """System tray application for FixPipeline."""
    
    def __init__(self):
        self.config = self.load_config()
        self.observer = None
        self.handler = None
        self.icon = None
        self.is_running = False
        
    def load_config(self):
        """Load configuration from file."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
            except Exception as e:
                print(f"Config load error: {e}")
        return DEFAULT_CONFIG.copy()
        
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Config save error: {e}")
            
    def create_icon_image(self):
        """Create a professional icon for FixPipeline."""
        # Create a 64x64 icon with professional design
        img = Image.new('RGB', (64, 64), color='#2E86AB')
        draw = ImageDraw.Draw(img)
        
        # Draw a professional gear/repair icon
        # Outer circle
        draw.ellipse([8, 8, 56, 56], outline='white', width=3)
        
        # Inner gear teeth
        for i in range(8):
            angle = i * 45
            x1 = 32 + 20 * (0.7 if i % 2 == 0 else 0.5)
            y1 = 32 + 20 * (0.7 if i % 2 == 0 else 0.5)
            x2 = 32 + 25 * (0.7 if i % 2 == 0 else 0.5)
            y2 = 32 + 25 * (0.7 if i % 2 == 0 else 0.5)
            draw.line([x1, y1, x2, y2], fill='white', width=2)
        
        # Center circle
        draw.ellipse([24, 24, 40, 40], outline='white', width=2)
        
        return img
        
    def start_monitoring(self):
        """Start file system monitoring."""
        if self.observer and self.observer.is_alive():
            return
            
        watch_dir = Path(self.config['watch_dir'])
        if not watch_dir.exists():
            print(f"Watch directory {watch_dir} does not exist!")
            return
            
        self.handler = FixPipelineHandler(self.config)
        self.observer = Observer()
        self.observer.schedule(self.handler, str(watch_dir), recursive=False)
        self.observer.start()
        self.is_running = True
        print(f"🔍 FixPipeline monitoring: {watch_dir}")
        
    def stop_monitoring(self):
        """Stop file system monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.is_running = False
            print("⏹️ FixPipeline monitoring stopped")
            
    def toggle_monitoring(self, icon, item):
        """Toggle monitoring on/off."""
        if self.is_running:
            self.handler.pause()
            self.stop_monitoring()
            item.text = "▶️ Resume Monitoring"
            icon.title = "FixPipeline (Paused)"
        else:
            self.start_monitoring()
            item.text = "⏸️ Pause Monitoring"
            icon.title = "FixPipeline (Running)"
            
    def open_settings(self, icon, item):
        """Open settings dialog."""
        from tkinter import filedialog, messagebox
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        new_dir = filedialog.askdirectory(
            title="Select folder to monitor",
            initialdir=self.config['watch_dir']
        )
        
        if new_dir:
            self.config['watch_dir'] = new_dir
            self.save_config()
            messagebox.showinfo("FixPipeline Settings", f"Watch directory changed to:\n{new_dir}")
            
    def show_status(self, icon, item):
        """Show current status."""
        status = "Running" if self.is_running else "Paused"
        watch_dir = self.config['watch_dir']
        target_files = len(self.config['target_files'])
        
        message = f"""FixPipeline Status

Status: {status}
Watching: {watch_dir}
Target files: {target_files}
Target files:
{chr(10).join(f'• {f}' for f in self.config['target_files'])}"""
        
        plyer.notification.notify(
            title="FixPipeline Status",
            message=message,
            timeout=10
        )
        
    def exit_app(self, icon, item):
        """Exit the application."""
        self.stop_monitoring()
        icon.stop()
        sys.exit(0)
        
    def create_menu(self):
        """Create the system tray menu."""
        status_text = "⏸️ Pause Monitoring" if self.is_running else "▶️ Resume Monitoring"
        
        menu = pystray.Menu(
            pystray.MenuItem("📊 Status", self.show_status),
            pystray.MenuItem(status_text, self.toggle_monitoring),
            pystray.MenuItem("⚙️ Settings", self.open_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌ Exit", self.exit_app)
        )
        return menu
        
    def run(self):
        """Run the tray application."""
        # Start monitoring
        self.start_monitoring()
        
        # Create and run tray icon
        icon_image = self.create_icon_image()
        menu = self.create_menu()
        
        self.icon = pystray.Icon(
            "FixPipeline",
            icon_image,
            menu=menu,
            title="FixPipeline (Running)"
        )
        
        print("🚀 FixPipeline started in system tray")
        print("Right-click the tray icon for options")
        
        try:
            self.icon.run()
        except KeyboardInterrupt:
            self.stop_monitoring()
            sys.exit(0)

def run_gui():
    """Run the manual GUI tool."""
    import tkinter as tk
    from tkinter import filedialog, messagebox
    
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

        messagebox.showinfo("FixPipeline", "\n".join(lines))

    root = tk.Tk()
    root.title("FixPipeline - Manual APK Converter")
    root.resizable(False, False)

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

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='FixPipeline - CircleCI APK Auto-Fixer')
    parser.add_argument('--gui', action='store_true', help='Open manual GUI tool')
    parser.add_argument('--version', action='version', version='FixPipeline 1.0.0')
    
    args = parser.parse_args()
    
    if args.gui:
        print("🚀 FixPipeline - Manual GUI Tool")
        run_gui()
    else:
        print("🚀 FixPipeline - System Tray App")
        print("=" * 50)
        
        # Check if already running
        try:
            import psutil
            current_process = psutil.Process()
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if (proc.info['name'] == 'python' and 
                        'fixpipeline' in ' '.join(proc.info['cmdline']) and
                        proc.info['pid'] != current_process.pid):
                        print("⚠️ FixPipeline is already running!")
                        print("Check your system tray for the icon.")
                        return
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except ImportError:
            pass
        
        # Create and run the app
        app = FixPipelineTray()
        app.run()

if __name__ == "__main__":
    main()
