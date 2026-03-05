# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║                     NPP AUTOSAVE v1.0.0                          ║
║         Intelligent autosave for Notepad++                       ║
╠══════════════════════════════════════════════════════════════════╣
║  Author:  Tadega                                                 ║
║  License: MIT (free to use, modify and share)                    ║
╠══════════════════════════════════════════════════════════════════╣
║  INSTALLATION:                                                   ║
║  1. Save to: %APPDATA%/Notepad++/plugins/config/                 ║
║              PythonScript/scripts/autosave.py                    ║
║  2. Plugins > PythonScript > Configuration > ATSTARTUP           ║
║  3. Restart Notepad++                                            ║
╠══════════════════════════════════════════════════════════════════╣
║  USAGE:                                                          ║
║  Line 1: Filename                                                ║
║  Saves automatically after 10 seconds of inactivity              ║
╚══════════════════════════════════════════════════════════════════╝
"""

__version__ = "1.0.0"
__author__ = "Tadega"
__license__ = "MIT"

from Npp import notepad, editor, console, NOTIFICATION, STATUSBARSECTION
import os
import io
import json
import shutil
import time
import threading
from datetime import datetime


# ══════════════════════════════════════════════════════════════════
# SETTINGS
# ══════════════════════════════════════════════════════════════════
BASE_DIR = os.path.expanduser("~/Documents/NPP")
BACKUP_DIR = os.path.join(BASE_DIR, "_backup")
OLD_DIR = os.path.join(BASE_DIR, "_old")
META_DIR = os.path.join(BASE_DIR, "_meta")
CONFIG_FILE = os.path.join(BASE_DIR, "config.txt")
LOG_FILE = os.path.join(BASE_DIR, "autosave.log")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
STATS_FILE = os.path.join(META_DIR, "stats.json")

DEFAULT_CONFIG = {
    "idle_time": 10,
    "max_backup_age_days": 30,
    "max_backups_per_file": 50,
    "show_notifications": False,
    "show_statusbar": True,
    "theme": "dark"
}


# ══════════════════════════════════════════════════════════════════
# INITIALIZATION
# ══════════════════════════════════════════════════════════════════
def init_folders():
    """Create necessary folders."""
    for d in [BASE_DIR, BACKUP_DIR, OLD_DIR, META_DIR]:
        if not os.path.exists(d):
            try:
                os.makedirs(d)
            except Exception as e:
                console.write("Could not create folder {}: {}\n".format(d, e))

init_folders()


# ══════════════════════════════════════════════════════════════════
# LOGGING
# ══════════════════════════════════════════════════════════════════
def log(message, level="INFO"):
    """Write to log file and console."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = u"[{}] [{}] {}".format(timestamp, level, message)
        
        try:
            with io.open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(entry + u"\n")
        except Exception:
            pass
        
        try:
            console.write(entry.encode("utf-8") + "\n")
        except Exception:
            try:
                console.write(str(entry) + "\n")
            except Exception:
                pass
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════
def create_default_config():
    """Create default config file."""
    try:
        with io.open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(u"# ══════════════════════════════════════════════════════════\n")
            f.write(u"# NPP Autosave Configuration v{}\n".format(__version__))
            f.write(u"# ══════════════════════════════════════════════════════════\n\n")
            f.write(u"# Seconds to wait after last keypress before saving\n")
            f.write(u"idle_time = {}\n\n".format(DEFAULT_CONFIG["idle_time"]))
            f.write(u"# Move backups older than X days to _old folder\n")
            f.write(u"max_backup_age_days = {}\n\n".format(DEFAULT_CONFIG["max_backup_age_days"]))
            f.write(u"# Maximum number of backups per file\n")
            f.write(u"max_backups_per_file = {}\n\n".format(DEFAULT_CONFIG["max_backups_per_file"]))
            f.write(u"# Show popup notification on save (true/false)\n")
            f.write(u"show_notifications = {}\n\n".format(str(DEFAULT_CONFIG["show_notifications"]).lower()))
            f.write(u"# Show save status in statusbar (true/false)\n")
            f.write(u"show_statusbar = {}\n\n".format(str(DEFAULT_CONFIG["show_statusbar"]).lower()))
            f.write(u"# Theme for index.html (dark/light)\n")
            f.write(u"theme = {}\n".format(DEFAULT_CONFIG["theme"]))
        log(u"Config created: {}".format(CONFIG_FILE))
    except Exception as e:
        log(u"Could not create config: {}".format(e), "ERROR")


def get_config_value(key, default=None):
    """Read value from config."""
    if default is None:
        default = DEFAULT_CONFIG.get(key)
    
    try:
        if not os.path.exists(CONFIG_FILE):
            create_default_config()
            return default
        
        with io.open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                
                k, v = line.split("=", 1)
                k = k.strip().lower()
                v = v.strip()
                
                if k == key.lower():
                    if v.lower() in ("true", "1", "yes", "on"):
                        return True
                    elif v.lower() in ("false", "0", "no", "off"):
                        return False
                    elif v.lower() in ("dark", "light"):
                        return v.lower()
                    try:
                        return int(v)
                    except ValueError:
                        return v
    except Exception:
        pass
    return default


def get_idle_time():
    """Get idle time setting."""
    return max(1, get_config_value("idle_time", DEFAULT_CONFIG["idle_time"]))


# ══════════════════════════════════════════════════════════════════
# STATUSBAR & NOTIFICATIONS
# ══════════════════════════════════════════════════════════════════
last_save_time = None

def update_statusbar(message):
    """Update Notepad++ statusbar."""
    if not get_config_value("show_statusbar", True):
        return
    try:
        notepad.setStatusBar(STATUSBARSECTION.DOCTYPE, message)
    except Exception:
        pass


def show_notification(title, message):
    """Show popup notification."""
    if not get_config_value("show_notifications", False):
        return
    try:
        notepad.messageBox(message, title, 0)
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════
# FILENAME HANDLING
# ══════════════════════════════════════════════════════════════════
def sanitize_filename(name):
    """Remove invalid characters from filename."""
    if not name:
        return ""
    
    invalid = '<>:"/\\|?*\r\n\t'
    for ch in invalid:
        name = name.replace(ch, "_")
    
    name = name.strip(". ")
    
    if len(name) > 80:
        name = name[:80]
    
    return name


def get_document_name(text, index):
    """Get document name from line 1."""
    if not text:
        return u"untitled_{}".format(index)
    
    first_line = text.split("\n", 1)[0].strip()
    name = sanitize_filename(first_line)
    
    if not name:
        return u"untitled_{}".format(index)
    
    return name


# ══════════════════════════════════════════════════════════════════
# STATISTICS
# ══════════════════════════════════════════════════════════════════
def load_stats():
    """Load statistics from file."""
    try:
        if os.path.exists(STATS_FILE):
            with io.open(STATS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    
    return {
        "total_saves": 0,
        "total_bytes_saved": 0,
        "first_save": None,
        "last_save": None,
        "saves_per_day": {}
    }


def save_stats(stats):
    """Save statistics to file."""
    try:
        with io.open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(u"Could not save stats: {}".format(e), "ERROR")


def update_stats(filename, size):
    """Update statistics after save."""
    try:
        stats = load_stats()
        
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        stats["total_saves"] += 1
        stats["total_bytes_saved"] += size
        stats["last_save"] = now.isoformat()
        
        if not stats["first_save"]:
            stats["first_save"] = now.isoformat()
        
        if today not in stats["saves_per_day"]:
            stats["saves_per_day"][today] = 0
        stats["saves_per_day"][today] += 1
        
        save_stats(stats)
        
    except Exception as e:
        log(u"Could not update stats: {}".format(e), "ERROR")


# ══════════════════════════════════════════════════════════════════
# BACKUP MANAGEMENT
# ══════════════════════════════════════════════════════════════════
def move_old_backups():
    """Move old backups to _old folder."""
    try:
        max_age = get_config_value("max_backup_age_days", DEFAULT_CONFIG["max_backup_age_days"])
        cutoff = time.time() - (max_age * 86400)
        moved = 0

        for filename in os.listdir(BACKUP_DIR):
            filepath = os.path.join(BACKUP_DIR, filename)
            
            if not os.path.isfile(filepath):
                continue
            
            if os.path.getmtime(filepath) < cutoff:
                dest = os.path.join(OLD_DIR, filename)
                
                if os.path.exists(dest):
                    name, ext = os.path.splitext(filename)
                    dest = os.path.join(OLD_DIR, "{}_{:%H%M%S%f}{}".format(name, datetime.now(), ext))
                
                shutil.move(filepath, dest)
                moved += 1

        if moved > 0:
            log(u"Moved {} backups to _old".format(moved))
            
    except Exception as e:
        log(u"Error moving backups: {}".format(e), "ERROR")


def limit_backups(name):
    """Limit number of backups per file."""
    try:
        max_count = get_config_value("max_backups_per_file", DEFAULT_CONFIG["max_backups_per_file"])
        prefix = name + "_"
        
        files = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith(prefix) and filename.endswith(".txt"):
                filepath = os.path.join(BACKUP_DIR, filename)
                files.append((os.path.getmtime(filepath), filepath, filename))
        
        if len(files) > max_count:
            files.sort()
            for _, filepath, filename in files[:len(files) - max_count]:
                dest = os.path.join(OLD_DIR, filename)
                if os.path.exists(dest):
                    name_part, ext = os.path.splitext(filename)
                    dest = os.path.join(OLD_DIR, "{}_{:%H%M%S%f}{}".format(name_part, datetime.now(), ext))
                shutil.move(filepath, dest)
                
    except Exception as e:
        log(u"Error limiting backups: {}".format(e), "ERROR")


# ══════════════════════════════════════════════════════════════════
# FILE OPERATIONS
# ══════════════════════════════════════════════════════════════════
def scan_files(directory):
    """Scan files in a directory."""
    files = []
    try:
        if not os.path.exists(directory):
            return files
        
        for filename in os.listdir(directory):
            if not filename.endswith(".txt"):
                continue
                
            filepath = os.path.join(directory, filename)
            if not os.path.isfile(filepath):
                continue
            
            files.append({
                "name": filename,
                "path": filepath,
                "mtime": os.path.getmtime(filepath),
                "size": os.path.getsize(filepath)
            })
        
        files.sort(key=lambda x: -x["mtime"])
    except Exception as e:
        log(u"Error scanning {}: {}".format(directory, e), "ERROR")
    
    return files


def format_size(bytes):
    """Format file size."""
    if bytes < 1024:
        return "{} B".format(bytes)
    elif bytes < 1024 * 1024:
        return "{:.1f} KB".format(bytes / 1024.0)
    else:
        return "{:.1f} MB".format(bytes / (1024.0 * 1024.0))


def format_time_ago(timestamp):
    """Format time ago."""
    diff = time.time() - timestamp
    
    if diff < 60:
        return "just nu"
    elif diff < 3600:
        return "{} min sedan".format(int(diff / 60))
    elif diff < 86400:
        return "{} tim sedan".format(int(diff / 3600))
    elif diff < 604800:
        return "{} dagar sedan".format(int(diff / 86400))
    else:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


# ══════════════════════════════════════════════════════════════════
# HTML INDEX GENERATOR
# ══════════════════════════════════════════════════════════════════
def generate_index():
    """Generate HTML index file."""
    try:
        main_files = scan_files(BASE_DIR)
        backup_files = scan_files(BACKUP_DIR)
        old_files = scan_files(OLD_DIR)
        
        stats = load_stats()
        total_size = sum(f["size"] for f in main_files + backup_files + old_files)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate statistics
        cutoff_7days = time.time() - (7 * 86400)
        recent_files = [f for f in main_files if f["mtime"] > cutoff_7days]
        largest_file = max(main_files, key=lambda x: x["size"]) if main_files else None
        
        avg_per_day = 0
        if stats.get("saves_per_day"):
            avg_per_day = sum(stats["saves_per_day"].values()) / max(1, len(stats["saves_per_day"]))
        
        theme = get_config_value("theme", "dark")
        body_class = "light-mode" if theme == "light" else ""
        
        html = generate_html_content(
            main_files, backup_files, old_files,
            stats, total_size, now, len(recent_files),
            largest_file, avg_per_day, body_class
        )
        
        with io.open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        
        log(u"Index updated ({} files)".format(len(main_files) + len(backup_files) + len(old_files)))
        
    except Exception as e:
        log(u"Error generating index: {}".format(e), "ERROR")


def generate_html_content(main_files, backup_files, old_files, stats, total_size, now, recent_count, largest_file, avg_per_day, body_class):
    """Generate complete HTML content."""
    
    def file_rows(files):
        rows = u""
        for f in files:
            url = "file:///" + f["path"].replace("\\", "/").replace(" ", "%20")
            date = datetime.fromtimestamp(f["mtime"]).strftime("%Y-%m-%d %H:%M")
            ago = format_time_ago(f["mtime"])
            size = format_size(f["size"])
            
            rows += u'''
                <tr class="file-row" data-name="{}">
                    <td><a href="{}" class="file-link">{}</a></td>
                    <td class="size">{}</td>
                    <td class="date" title="{}">{}</td>
                </tr>'''.format(f["name"].lower(), url, f["name"], size, date, ago)
        return rows
    
    html = u'''<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NPP Autosave v{version}</title>
    <style>
        :root {{
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --bg-card: rgba(255,255,255,0.05);
            --text-primary: #eee;
            --text-secondary: #888;
            --accent: #4fc3f7;
            --border: #333;
        }}
        
        body.light-mode {{
            --bg-primary: #f5f7fa;
            --bg-secondary: #e8eef5;
            --bg-card: rgba(0,0,0,0.05);
            --text-primary: #333;
            --text-secondary: #666;
            --border: #ddd;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            color: var(--text-primary);
            padding: 20px;
            min-height: 100vh;
            transition: all 0.3s ease;
        }}
        
        .container {{ max-width: 900px; margin: 0 auto; }}
        
        header {{
            text-align: center;
            padding: 25px 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 25px;
            position: relative;
        }}
        
        .logo {{ font-size: 2.5em; margin-bottom: 5px; }}
        h1 {{ color: var(--accent); font-size: 1.8em; margin-bottom: 5px; }}
        .version {{ color: var(--text-secondary); font-size: 0.85em; }}
        .updated {{ color: var(--text-secondary); font-size: 0.85em; margin-top: 5px; }}
        
        .theme-toggle {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 8px 15px;
            border-radius: 20px;
            color: var(--text-primary);
            cursor: pointer;
            font-size: 1.1em;
        }}
        
        .theme-toggle:hover {{ background: var(--accent); color: #000; }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 12px;
            margin: 20px 0;
        }}
        
        .stat {{
            background: var(--bg-card);
            padding: 12px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid var(--border);
        }}
        
        .stat-num {{ font-size: 1.4em; color: var(--accent); font-weight: bold; }}
        .stat-label {{ font-size: 0.75em; color: var(--text-secondary); margin-top: 2px; }}
        
        .stats-panel {{
            background: var(--bg-card);
            border-radius: 10px;
            padding: 18px;
            margin: 20px 0;
            border: 1px solid var(--border);
        }}
        
        .stats-panel h3 {{ color: var(--accent); margin-bottom: 12px; font-size: 1em; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
        }}
        
        .stats-item-label {{ color: var(--text-secondary); font-size: 0.8em; }}
        .stats-item-value {{ color: var(--text-primary); font-size: 1.1em; font-weight: 500; }}
        
        .search {{
            margin: 20px 0;
            position: relative;
        }}
        
        .search input {{
            width: 100%;
            padding: 12px 20px 12px 45px;
            border: 1px solid var(--border);
            border-radius: 25px;
            background: var(--bg-card);
            color: var(--text-primary);
            font-size: 1em;
        }}
        
        .search input:focus {{
            outline: none;
            border-color: var(--accent);
        }}
        
        .search::before {{
            content: "🔍";
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
        }}
        
        .section {{
            background: var(--bg-card);
            border-radius: 10px;
            margin-bottom: 15px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        
        .section-header {{
            padding: 12px 18px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .section-header:hover {{ background: rgba(255,255,255,0.05); }}
        .section-header.main {{ background: rgba(79,195,247,0.12); }}
        .section-header.backup {{ background: rgba(255,193,7,0.12); }}
        .section-header.old {{ background: rgba(158,158,158,0.12); }}
        
        .section-title {{ font-weight: 600; display: flex; align-items: center; gap: 8px; }}
        .section-count {{ background: rgba(255,255,255,0.15); padding: 2px 10px; border-radius: 10px; font-size: 0.8em; }}
        
        .toggle-icon {{ transition: transform 0.2s; font-size: 0.7em; }}
        .section-header.collapsed .toggle-icon {{ transform: rotate(-90deg); }}
        
        .section-content {{ display: none; padding: 8px 12px; }}
        .section-content.open {{ display: block; }}
        
        table {{ width: 100%; border-collapse: collapse; }}
        .file-row:hover {{ background: rgba(255,255,255,0.08); }}
        td {{ padding: 8px 6px; border-bottom: 1px solid var(--border); }}
        .file-row:last-child td {{ border-bottom: none; }}
        
        .file-link {{ color: var(--text-primary); text-decoration: none; }}
        .file-link:hover {{ color: var(--accent); text-decoration: underline; }}
        
        .size, .date {{ text-align: right; color: var(--text-secondary); font-size: 0.8em; white-space: nowrap; }}
        
        footer {{
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            font-size: 0.8em;
            border-top: 1px solid var(--border);
            margin-top: 25px;
        }}
        
        footer a {{ color: var(--accent); text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
        
        .no-results {{ text-align: center; padding: 30px; color: var(--text-secondary); display: none; }}
        .empty-state {{ text-align: center; padding: 20px; color: var(--text-secondary); }}
    </style>
</head>
<body class="{body_class}">
    <div class="container">
        <header>
            <div class="logo">📁</div>
            <h1>NPP Autosave</h1>
            <div class="version">v{version}</div>
            <div class="updated">Uppdaterad: {now}</div>
            <button class="theme-toggle" onclick="toggleTheme()">🌓</button>
        </header>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-num">{main_count}</div>
                <div class="stat-label">Dokument</div>
            </div>
            <div class="stat">
                <div class="stat-num">{backup_count}</div>
                <div class="stat-label">Backups</div>
            </div>
            <div class="stat">
                <div class="stat-num">{old_count}</div>
                <div class="stat-label">Arkiv</div>
            </div>
            <div class="stat">
                <div class="stat-num">{total_size}</div>
                <div class="stat-label">Storlek</div>
            </div>
            <div class="stat">
                <div class="stat-num">{total_saves}</div>
                <div class="stat-label">Sparningar</div>
            </div>
        </div>
        
        <div class="stats-panel">
            <h3>📊 Statistik</h3>
            <div class="stats-grid">
                <div>
                    <div class="stats-item-label">Senaste 7 dagar</div>
                    <div class="stats-item-value">{recent_count} filer</div>
                </div>
                <div>
                    <div class="stats-item-label">Snitt/dag</div>
                    <div class="stats-item-value">{avg_per_day:.1f} sparningar</div>
                </div>
                <div>
                    <div class="stats-item-label">Största fil</div>
                    <div class="stats-item-value">{largest_file}</div>
                </div>
                <div>
                    <div class="stats-item-label">Total sparat</div>
                    <div class="stats-item-value">{total_bytes_saved}</div>
                </div>
            </div>
        </div>
        
        <div class="search">
            <input type="text" id="search" placeholder="Sök filer..." oninput="filterFiles()">
        </div>
        
        <main>
            <div class="section">
                <div class="section-header main" onclick="toggleSection('main')">
                    <span class="section-title">📄 Dokument</span>
                    <span><span class="section-count">{main_count}</span> <span class="toggle-icon">▼</span></span>
                </div>
                <div class="section-content open" id="content-main">
                    {main_content}
                </div>
            </div>
            
            <div class="section">
                <div class="section-header backup collapsed" onclick="toggleSection('backup')">
                    <span class="section-title">💾 Backup</span>
                    <span><span class="section-count">{backup_count}</span> <span class="toggle-icon">▼</span></span>
                </div>
                <div class="section-content" id="content-backup">
                    {backup_content}
                </div>
            </div>
            
            <div class="section">
                <div class="section-header old collapsed" onclick="toggleSection('old')">
                    <span class="section-title">📦 Arkiv</span>
                    <span><span class="section-count">{old_count}</span> <span class="toggle-icon">▼</span></span>
                </div>
                <div class="section-content" id="content-old">
                    {old_content}
                </div>
            </div>
        </main>
        
        <div class="no-results" id="no-results">😕 Inga filer matchade</div>
        
        <footer>
            <a href="file:///{config}">⚙️ Config</a> | 
            <a href="file:///{log}">📋 Logg</a> | 
            <a href="file:///{folder}">📂 Öppna mapp</a>
            <br><br>
            NPP Autosave v{version} &copy; {year} {author}
        </footer>
    </div>
    
    <script>
        function toggleTheme() {{
            document.body.classList.toggle('light-mode');
            localStorage.setItem('npp-theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
        }}
        
        (function() {{
            if (localStorage.getItem('npp-theme') === 'light') document.body.classList.add('light-mode');
        }})();
        
        function toggleSection(id) {{
            var header = event.currentTarget;
            var content = document.getElementById('content-' + id);
            header.classList.toggle('collapsed');
            content.classList.toggle('open');
        }}
        
        function filterFiles() {{
            var q = document.getElementById('search').value.toLowerCase();
            var rows = document.querySelectorAll('.file-row');
            var visible = 0;
            
            rows.forEach(function(row) {{
                var match = row.getAttribute('data-name').includes(q);
                row.style.display = match ? '' : 'none';
                if (match) visible++;
            }});
            
            document.getElementById('no-results').style.display = (q && visible === 0) ? 'block' : 'none';
            
            if (q) {{
                document.querySelectorAll('.section-content').forEach(function(c) {{ c.classList.add('open'); }});
                document.querySelectorAll('.section-header').forEach(function(h) {{ h.classList.remove('collapsed'); }});
            }}
        }}
    </script>
</body>
</html>'''.format(
        version=__version__,
        author=__author__,
        year=datetime.now().year,
        now=now,
        body_class=body_class,
        main_count=len(main_files),
        backup_count=len(backup_files),
        old_count=len(old_files),
        total_size=format_size(total_size),
        total_saves=stats.get("total_saves", 0),
        recent_count=recent_count,
        avg_per_day=avg_per_day,
        largest_file=largest_file["name"] if largest_file else "N/A",
        total_bytes_saved=format_size(stats.get("total_bytes_saved", 0)),
        main_content=u"<table>{}</table>".format(file_rows(main_files)) if main_files else u'<div class="empty-state">Inga dokument än</div>',
        backup_content=u"<table>{}</table>".format(file_rows(backup_files)) if backup_files else u'<div class="empty-state">Inga backups än</div>',
        old_content=u"<table>{}</table>".format(file_rows(old_files)) if old_files else u'<div class="empty-state">Inga arkiv än</div>',
        config=CONFIG_FILE.replace("\\", "/"),
        log=LOG_FILE.replace("\\", "/"),
        folder=BASE_DIR.replace("\\", "/")
    )
    
    return html


# ══════════════════════════════════════════════════════════════════
# SAVE OPERATIONS
# ══════════════════════════════════════════════════════════════════
def save_current_buffer():
    """Save current buffer."""
    global last_save_time
    
    try:
        if not editor.getModify():
            return False
        
        text = editor.getText()
        if not text:
            return False
        
        if isinstance(text, bytes):
            text = text.decode("utf-8", errors="replace")
        
        buffer_id = notepad.getCurrentBufferID()
        files = notepad.getFiles()
        index = 0
        for i, f in enumerate(files):
            if len(f) >= 2 and f[1] == buffer_id:
                index = i
                break
        
        name = get_document_name(text, index)
        
        # Save main file
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = u"{}_{}.txt".format(name, date_str)
        filepath = os.path.join(BASE_DIR, filename)
        
        with io.open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        
        # Save backup
        ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_name = u"{}_{}.txt".format(name, ts)
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        
        with io.open(backup_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        editor.setSavePoint()
        update_stats(filename, len(text))
        limit_backups(name)
        
        last_save_time = datetime.now()
        update_statusbar(u"✓ Sparad {}".format(last_save_time.strftime("%H:%M:%S")))
        show_notification(u"Autosave", u"Sparad: {}".format(filename))
        
        log(u"Saved: {}".format(filename))
        generate_index()
        
        return True
        
    except Exception as e:
        log(u"Error saving: {}".format(e), "ERROR")
        update_statusbar(u"✗ Fel vid sparning")
        return False


# ══════════════════════════════════════════════════════════════════
# MANUAL COMMANDS
# ══════════════════════════════════════════════════════════════════
def manual_save():
    """Manual save command."""
    if save_current_buffer():
        notepad.messageBox(u"✓ Fil sparad!", u"NPP Autosave", 0)
    else:
        notepad.messageBox(u"Inget att spara", u"NPP Autosave", 0)


def open_index():
    """Open index in browser."""
    import subprocess
    try:
        generate_index()
        subprocess.Popen(['start', '', INDEX_FILE], shell=True)
    except Exception as e:
        log(u"Could not open index: {}".format(e), "ERROR")


def open_config():
    """Open config in Notepad++."""
    if not os.path.exists(CONFIG_FILE):
        create_default_config()
    notepad.open(CONFIG_FILE)


def open_folder():
    """Open NPP folder in Explorer."""
    import subprocess
    try:
        subprocess.Popen(['explorer', BASE_DIR])
    except Exception as e:
        log(u"Could not open folder: {}".format(e), "ERROR")


# ══════════════════════════════════════════════════════════════════
# IDLE-BASED AUTOSAVE
# ══════════════════════════════════════════════════════════════════
class IdleAutoSaver:
    """Saves after X seconds of inactivity."""
    
    def __init__(self):
        self.timer = None
        self.last_change = 0
        self.pending_save = False
        self.lock = threading.Lock()
        self.cycle_count = 0
        self.running = False
    
    def on_text_changed(self, args):
        """Called on every text change."""
        with self.lock:
            self.last_change = time.time()
            self.pending_save = True
            
            if self.timer:
                self.timer.cancel()
            
            idle_time = get_idle_time()
            self.timer = threading.Timer(idle_time, self._check_and_save)
            self.timer.daemon = True
            self.timer.start()
            
            update_statusbar(u"⏳ Sparas om {}s...".format(idle_time))
    
    def _check_and_save(self):
        """Check and save if inactive."""
        with self.lock:
            if not self.pending_save:
                return
            
            elapsed = time.time() - self.last_change
            idle_time = get_idle_time()
            
            if elapsed >= idle_time:
                self.pending_save = False
                self._do_save()
            else:
                remaining = idle_time - elapsed
                self.timer = threading.Timer(remaining, self._check_and_save)
                self.timer.daemon = True
                self.timer.start()
    
    def _do_save(self):
        """Perform save."""
        try:
            save_current_buffer()
            
            self.cycle_count += 1
            if self.cycle_count >= 50:
                self.cycle_count = 0
                move_old_backups()
                
        except Exception as e:
            log(u"Idle save error: {}".format(e), "ERROR")
    
    def start(self):
        """Start idle monitoring."""
        if self.running:
            return
        
        try:
            editor.callback(self.on_text_changed, [NOTIFICATION.MODIFIED])
            self.running = True
            log(u"IdleAutoSaver started ({}s)".format(get_idle_time()))
            update_statusbar(u"✓ Autosave aktiv")
        except Exception as e:
            log(u"Error starting: {}".format(e), "ERROR")
    
    def stop(self):
        """Stop idle monitoring."""
        try:
            self.running = False
            if self.timer:
                self.timer.cancel()
                self.timer = None
            editor.clearCallbacks([NOTIFICATION.MODIFIED])
            log(u"IdleAutoSaver stopped")
        except Exception as e:
            log(u"Error stopping: {}".format(e), "ERROR")


# ══════════════════════════════════════════════════════════════════
# STARTUP
# ══════════════════════════════════════════════════════════════════
try:
    _autosaver.stop()
    time.sleep(0.3)
except NameError:
    pass
except Exception:
    pass

_autosaver = IdleAutoSaver()
_autosaver.start()

generate_index()

log(u"═" * 50)
log(u"NPP Autosave v{} loaded".format(__version__))
log(u"═" * 50)
log(u"Folder:    {}".format(BASE_DIR))
log(u"Idle time: {}s".format(get_idle_time()))
log(u"═" * 50)
log(u"Commands: manual_save(), open_index(), open_config(), open_folder()")
log(u"═" * 50)