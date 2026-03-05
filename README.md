# 📁 NPP Autosave

Intelligent autosave plugin för Notepad++ som sparar automatiskt efter inaktivitet.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-2.7-yellow)

## ✨ Funktioner

- 💾 **Smart sparning** - Sparar 10 sekunder efter du slutat skriva
- 📊 **Statistik** - Spårar antal sparningar, filstorlek, etc
- 🔍 **HTML-index** - Sökbar filöversikt med dark/light mode
- 📦 **Backup-rotation** - Automatisk arkivering av gamla backups
- ⚙️ **Konfigurerbart** - Enkla inställningar via config-fil
- 📈 **Statusbar** - Visar sparstatus direkt i Notepad++

## 📥 Installation

### Steg 1: Installera PythonScript plugin

1. Öppna Notepad++
2. **Plugins** → **Plugins Admin**
3. Sök efter **"PythonScript"**
4. Installera och starta om Notepad++

### Steg 2: Installera Autosave

**Alternativ A: Manuell installation**

1. Ladda ner [`autosave.py`](https://raw.githubusercontent.com/DITTANVÄNDARNAMN/npp-autosave/main/autosave.py)
2. Placera i: `%APPDATA%\Notepad++\plugins\config\PythonScript\scripts\`
3. **Plugins** → **PythonScript** → **Configuration**
4. Välj **ATSTARTUP** för `autosave.py`
5. Starta om Notepad++

**Alternativ B: Med installer** *(kommer snart)*

```bash
python install.py