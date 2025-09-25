# FixPipeline

**Professional CircleCI APK Auto-Fixer**

Automatically converts CircleCI APK downloads from `.zip` to `.apk` files for QA teams.

## 🎯 Problem Solved

When downloading APK files from CircleCI artifacts:
- Chrome/Firefox save them as `.zip` files
- Manual renaming doesn't work for installation
- QA teams need to test 4 specific files repeatedly

## 🚀 Installation

### Option 1: pip Install (Recommended)

```bash
# Install from GitHub (works like any pip package)
pip install git+https://github.com/subhadip-unn/FixPipeline.git

# Then use
fixpipeline              # System tray app
fixpipeline --gui         # Manual GUI tool
```

### Option 2: .deb Package (Linux)

```bash
# Download .deb from GitHub Releases
wget https://github.com/subhadip-unn/FixPipeline/releases/latest/download/fixpipeline_1.0.0-1_all.deb

# Install like any software
sudo dpkg -i fixpipeline_1.0.0-1_all.deb
sudo apt -f install  # Fix dependencies if needed

# Use
fixpipeline
```

### Option 3: Direct Run (Development)

```bash
# Clone and run
git clone https://github.com/subhadip-unn/FixPipeline.git
cd FixPipeline
pip install -r requirements.txt
python fixpipeline.py
```

## 🎯 Usage

### System Tray App (Recommended)

```bash
fixpipeline
```

**Features:**
- ✅ Monitors Downloads folder automatically
- ✅ Converts your 4 specific APK files
- ✅ System tray integration (pause/resume/exit)
- ✅ Professional notifications
- ✅ Auto-start on login
- ✅ Settings (change watch folder)
- ✅ Works with any browser

### Manual GUI Tool

```bash
fixpipeline --gui
```

**For one-time conversions:**
- Select `.zip` files
- Automatically converts to `.apk`
- Shows conversion results

## 🎯 Target Files

FixPipeline automatically converts these 4 files:
- `app-production-release.apk`
- `app-staging-release.apk` 
- `app-production-debug.apk`
- `app-staging-debug.apk`

## 🔧 Requirements

- Python 3.7+
- Dependencies: `pystray`, `pillow`, `plyer`, `watchdog`, `psutil`

## 💡 Why This Works

The system-level `os.rename()` operation properly updates file metadata, making the converted `.apk` files installable via ADB, unlike manual renaming.

## 📦 For QA Teams

### Easy Installation (No Technical Knowledge Required)

**Option A: pip Install (Recommended)**
```bash
pip install git+https://github.com/subhadip-unn/FixPipeline.git
fixpipeline
```

**Option B: .deb Package (Linux)**
```bash
# Download from GitHub Releases
wget https://github.com/subhadip-unn/FixPipeline/releases/latest/download/fixpipeline_1.0.0-1_all.deb
sudo dpkg -i fixpipeline_1.0.0-1_all.deb
fixpipeline
```

**That's it!** No venv, no manual setup - works like any professional software.

## 🔒 Security

- ✅ No sensitive data
- ✅ No network connections
- ✅ Only monitors local Downloads folder
- ✅ Safe for corporate use
