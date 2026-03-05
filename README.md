📁 NPP Autosave
Intelligent autosave plugin for Notepad++ that automatically saves your work.

✨ Features
Feature	Description
💾 Smart Saving	Saves active tab 10 seconds after you stop typing
🔄 Interval Backup	Saves ALL tabs every 5 minutes
📁 Dual Save Mode	Existing files → original location, New files → NPP folder
📊 Statistics	Tracks saves, file sizes, and daily activity
🔍 HTML Index	Searchable file browser with dark/light theme
📦 Backup Rotation	Auto-archive old backups after 30 days
⚙️ Configurable	Simple config.txt for all settings
📥 Installation
Step 1: Install PythonScript Plugin
Open Notepad++
Go to: Plugins → Plugins Admin
Search: PythonScript
Click Install
Restart Notepad++
Step 2: Download Script
Download autosave.py from:

https://github.com/Tokke2/npp-autosave/releases

Place it here:

%APPDATA%\Notepad++\plugins\config\PythonScript\scripts\autosave.py

Step 3: Enable Autostart
Go to: Plugins → PythonScript → Configuration
Find: autosave.py in the list
Set Initialisation to: ATSTARTUP
Click OK
Restart Notepad++
Step 4: Verify Installation
Open console: Plugins → PythonScript → Show Console

You should see:

════════════════════════════════════════════════════════════
NPP Autosave v1.2.0 loaded
© 2026 Rickard Längkvist
════════════════════════════════════════════════════════════
Folder: C:\Users\YourName\Documents\NPP
Idle time: 10s (active tab)
Interval: 300s / 5min (all tabs)
════════════════════════════════════════════════════════════

📖 How It Works
Save Logic
┌─────────────────────────────────────────────────┐
│ FILE SAVE DECISION │
├─────────────────────────────────────────────────┤
│ │
│ Is file already saved to disk? │
│ │
│ YES NO │
│ │ │ │
│ ▼ ▼ │
│ ┌───────────┐ ┌─────────────┐ │
│ │ Save to │ │ Save to │ │
│ │ ORIGINAL │ │ NPP folder │ │
│ │ location │ │ Line 1 = │ │
│ │ │ │ filename │ │
│ └───────────┘ └─────────────┘ │
│ │ │ │
│ └──────────┬─────────────┘ │
│ ▼ │
│ ┌─────────────┐ │
│ │ Create │ │
│ │ backup copy │ │
│ └─────────────┘ │
│ │
└─────────────────────────────────────────────────┘

Two Save Modes
Mode	Trigger	Saves	Timing
Idle	Stop typing	Active tab	10 seconds
Interval	Timer	All tabs	Every 5 minutes
💡 Usage Examples
Example 1: New Document
Open new tab (Ctrl+N)
Type on line 1: My Notes
Type content below
Stop typing, wait 10 seconds
File saved as: My Notes_2026-03-05.txt
Example 2: Existing File
Open: C:\Projects\readme.txt
Make changes
Stop typing, wait 10 seconds
File saved to: C:\Projects\readme.txt (same location)
Backup created in: ~/Documents/NPP/_backup/
📂 Folder Structure
C:\Users\YourName\Documents\NPP
│
├── index.html ← Open in browser to view files
├── config.txt ← Settings
├── autosave.log ← Activity log
│
├── My Notes_2026-03-05.txt ← Saved documents
├── Todo List_2026-03-05.txt
│
├── _backup/ ← Recent backups (0-30 days)
│ ├── My Notes_2026-03-05_143022.txt
│ └── My Notes_2026-03-05_150133.txt
│
├── _old/ ← Archived backups (30+ days)
│ └── My Notes_2026-02-01_120000.txt
│
└── _meta/
└── stats.json ← Statistics data

⚙️ Configuration
Edit: C:\Users\YourName\Documents\NPP\config.txt

Seconds after typing stops to save active tab
idle_time = 10

Seconds between saving ALL tabs (300 = 5 minutes)
interval_time = 300

Move backups older than X days to _old folder
max_backup_age_days = 30

Max backups per file in _backup folder
max_backups_per_file = 50

Show popup when saving (true/false)
show_notifications = false

Show status in statusbar (true/false)
show_statusbar = true

Theme for index.html (dark/light)
theme = dark

🎯 Console Commands
Open console: Plugins → PythonScript → Show Console

Command	Description
manual_save()	Save active tab now
manual_save_all()	Save all tabs now
open_index()	Open index in browser
open_config()	Open config file
open_folder()	Open NPP folder in Explorer
_autosaver.stop()	Stop autosave
_autosaver.start()	Restart autosave
📊 HTML Index
Open: C:\Users\YourName\Documents\NPP\index.html

Features:

🔍 Search files instantly
🌓 Dark/Light theme toggle
🔗 Click to open any file
📈 Statistics dashboard
📁 Filter by folder
🐛 Troubleshooting
Script not loading
Check: Plugins → PythonScript → Configuration
Verify autosave.py is listed
Verify ATSTARTUP is selected
Restart Notepad++
Files not saving
Check permissions on folder:

C:\Users\YourName\Documents\NPP\

Where are my files?
Run command in console:

open_folder()

📜 Changelog
v1.2.0
Dual save mode (original location vs NPP folder)
Interval save for all tabs every 5 minutes
Improved file detection
Dynamic copyright year
v1.1.0
Idle-based autosave
HTML index with search
Statistics tracking
Dark/Light theme
Backup rotation
v1.0.0
Initial release
📄 License
MIT License

Copyright (c) 2026 Rickard Längkvist

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

👤 Author
Rickard Längkvist

GitHub: https://github.com/Tokke2

🔗 Links
Repository: https://github.com/Tokke2/npp-autosave

Issues: https://github.com/Tokke2/npp-autosave/issues

Releases: https://github.com/Tokke2/npp-autosave/releases

⭐ Star this repo if you find it useful!