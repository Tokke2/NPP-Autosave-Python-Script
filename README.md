📁 NPP Autosave
Intelligent autosave plugin for Notepad++ that automatically saves your work after inactivity.

Version
License
Python

✨ Features
💾 Smart Saving - Saves active tab 10 seconds after you stop typing
🔄 Interval Backup - Saves ALL tabs every 5 minutes
📁 Dual Save Mode - Already saved files update in place, new files go to NPP folder
📊 Statistics - Tracks save count, file size, and activity
🔍 HTML Index - Searchable file overview with dark/light theme
📦 Backup Rotation - Automatic archiving of old backups (30 days)
⚙️ Configurable - Easy settings via config file
📈 Statusbar - Shows save status directly in Notepad++
📥 Installation
Step 1: Install PythonScript Plugin
Open Notepad++
Go to Plugins → Plugins Admin
Search for "PythonScript"
Install and restart Notepad++
Step 2: Install NPP Autosave
Option A: Manual Installation

Download autosave.py
Place in: %APPDATA%\Notepad++\plugins\config\PythonScript\scripts\
Open Plugins → PythonScript → Configuration
Select ATSTARTUP for autosave.py
Restart Notepad++
Option B: Quick Install Script (coming soon)

Bash

python install.py
📖 Usage
How Files Are Saved
NPP Autosave uses intelligent dual-mode saving:

text

┌─────────────────────────────────────────────────────────────┐
│                    FILE SAVE LOGIC                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Is the file already saved to disk?                        │
│                                                             │
│   ┌──────────┐                    ┌──────────┐             │
│   │   YES    │                    │    NO    │             │
│   │ (exists) │                    │ (new tab)│             │
│   └────┬─────┘                    └────┬─────┘             │
│        │                               │                    │
│        ▼                               ▼                    │
│   ┌─────────────────┐      ┌─────────────────────┐         │
│   │ Save to SAME    │      │ Save to NPP folder  │         │
│   │ location        │      │ Filename = Line 1   │         │
│   │                 │      │ + date stamp        │         │
│   │ notepad.save()  │      │                     │         │
│   └─────────────────┘      └─────────────────────┘         │
│        │                               │                    │
│        └──────────┬────────────────────┘                    │
│                   ▼                                         │
│          ┌────────────────┐                                │
│          │ Create backup  │                                │
│          │ in _backup/    │                                │
│          └────────────────┘                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
Examples
Scenario 1: New Document

Create new tab in Notepad++
Type on line 1: Shopping List
Type your content below
Wait 10 seconds → Automatically saved as:
text

~/Documents/NPP/Shopping List_2026-03-05.txt
Scenario 2: Existing File

Open C:\Projects\readme.txt
Make changes
Wait 10 seconds → Saved to C:\Projects\readme.txt (same location)
Backup created in ~/Documents/NPP/_backup/
Scenario 3: Multiple Tabs

You have 5 tabs open (mix of new and saved files)
Every 5 minutes → ALL tabs are saved automatically
No need to manually save each one
⚙️ Configuration
Edit ~/Documents/NPP/config.txt:

ini

# Seconds to wait after typing stops (saves active tab)
idle_time = 10

# Seconds between saving ALL tabs (300 = 5 minutes)
interval_time = 300

# Move backups older than X days to _old folder
max_backup_age_days = 30

# Maximum number of backups per file in _backup
max_backups_per_file = 50

# Show popup notification when saving (true/false)
show_notifications = false

# Show save status in statusbar (true/false)
show_statusbar = true

# Theme for index.html (dark/light)
theme = dark
📂 File Structure
text

~/Documents/NPP/
├── index.html                    ← Click to view all files in browser
├── config.txt                    ← Settings
├── autosave.log                  ← Activity log
├── Shopping List_2026-03-05.txt  ← Saved files (from new tabs)
├── Notes_2026-03-05.txt
├── _backup/                      ← Recent backups (last 30 days)
│   ├── Shopping List_2026-03-05_143022.txt
│   ├── Shopping List_2026-03-05_150133.txt
│   └── Notes_2026-03-05_141555.txt
├── _old/                         ← Archived backups (30+ days old)
│   └── Shopping List_2026-02-01_120000.txt
└── _meta/
    └── stats.json                ← Statistics
🎯 Console Commands
Run in Plugins → PythonScript → Show Console:

Python

# Save active tab immediately
manual_save()

# Save all open tabs immediately
manual_save_all()

# Open index in web browser
open_index()

# Open config in Notepad++
open_config()

# Open NPP folder in Windows Explorer
open_folder()

# Stop autosave (if needed)
_autosaver.stop()

# Restart autosave
_autosaver.start()
🔧 How It Works
Two Save Modes
Mode	Trigger	What Gets Saved	When
Idle Save	Stop typing	Active tab only	10s after last keypress
Interval Save	Timer	ALL open tabs	Every 5 minutes
Save Decision Tree
text

┌─────────────────────────────────────────────────────────────┐
│ User stops typing                                           │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
           ⏱️ Wait 10 seconds (idle_time)
                       │
                       ▼
           ┌──────────────────────┐
           │ File already saved?  │
           └──────┬───────────────┘
                  │
         ┌────────┴────────┐
         ▼                 ▼
    ┌────────┐        ┌─────────┐
    │  YES   │        │   NO    │
    └───┬────┘        └────┬────┘
        │                  │
        ▼                  ▼
  Update at          Save to NPP/
  original           (line 1 as
  location           filename)
        │                  │
        └────────┬─────────┘
                 ▼
         Create backup copy
                 │
                 ▼
         Update statistics
                 │
                 ▼
           ✅ Done!
📊 Statistics Dashboard
Open index.html to see:

Total number of saves
Files saved per day
Total data saved
Recent activity (last 7 days)
Largest files
Search and filter capabilities
Features of index.html:
🔍 Search - Find files instantly
🌓 Dark/Light Mode - Toggle theme (preference saved)
📱 Responsive - Works on any screen size
🔗 Clickable Links - Open files directly from browser
📈 Statistics - Visual overview of your activity
🐛 Troubleshooting
Script not starting automatically
Check installation:

text

1. Plugins → PythonScript → Configuration
2. Verify "autosave.py" is listed
3. Ensure ATSTARTUP is checked
4. Restart Notepad++
Verify it's running:

text

Plugins → PythonScript → Show Console

You should see:
════════════════════════════════════════════════════════════
NPP Autosave v1.2.0 loaded
© 2026 Rickard Längkvist
════════════════════════════════════════════════════════════
Files not saving
Check console for errors:

text

Plugins → PythonScript → Show Console
Common issues:

❌ PythonScript plugin not installed → Install from Plugins Admin
❌ Script in wrong folder → Must be in PythonScript\scripts\
❌ Permission issues → Ensure ~/Documents/NPP is writable
Where are my files?
Default location:

text

Windows: C:\Users\YourName\Documents\NPP\
Quick access:
Run in console: open_folder()

🤝 Contributing
Contributions are welcome!

Fork the project
Create a feature branch: git checkout -b feature/amazing-feature
Commit your changes: git commit -m 'Add amazing feature'
Push to branch: git push origin feature/amazing-feature
Open a Pull Request
📜 Changelog
v1.2.0 (2026-03-05)
✅ Dual save mode (original location vs NPP folder)
✅ Interval save for all tabs (every 5 minutes)
✅ Improved file detection logic
✅ Dynamic copyright
v1.1.0 (2026-03-05)
✅ Idle-based autosave (10s after typing stops)
✅ HTML index with search
✅ Statistics tracking
✅ Dark/Light theme toggle
✅ Backup rotation
v1.0.0 (2026-03-04)
✅ Initial release
📄 License
MIT License - Free to use, modify, and distribute.

See LICENSE for details.

👤 Author
Rickard Längkvist

GitHub: @rickard-langkvist
🙏 Acknowledgments
PythonScript plugin by Dave Brotherstone
Notepad++ by Don Ho
Inspired by the need for reliable autosave in text editing
💡 Tips & Tricks
Best Practices
Use descriptive line 1 - This becomes the filename for new documents

text

Good: "Project Meeting Notes"
Bad:  "asdfjkl"
Check the HTML index - Quickly find old files and backups

Adjust idle_time - If 10s is too fast/slow, edit config.txt

Review backups periodically - Check _backup/ for recovery needs

Enable notifications - Set show_notifications = true for confirmation

Advanced Usage
Custom save locations:
The script saves existing files in their original location, but new files always go to ~/Documents/NPP/. If you want a different location, modify BASE_DIR in the script.

Integration with version control:
Keep ~/Documents/NPP/ in a Git repository for automatic version history of your notes and documents.

Network drives:
Works with network drives if already saved there. New files still go to local NPP folder.

⭐ Like this project? Give it a star!

🐛 Found a bug? Open an issue

💬 Questions? Start a discussion
