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
# Install from local directory
pip install -e .

# Or install from GitHub
pip install git+https://github.com/company/fixpipeline.git
```

### Option 2: Direct Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
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

## 📦 Distribution

### For QA Teams:

1. **Simple ZIP distribution:**
   ```bash
   zip -r fixpipeline.zip . -x "venv/*" "__pycache__/*" "*.pyc"
   ```

2. **QA Team Instructions:**
   - Download `fixpipeline.zip`
   - Extract anywhere
   - Run `python fixpipeline.py`
   - Look for FixPipeline icon in system tray

### For Technical Teams:

```bash
pip install fixpipeline
fixpipeline
```

## 🔒 Security

- ✅ No sensitive data
- ✅ No network connections
- ✅ Only monitors local Downloads folder
- ✅ Safe for corporate use
