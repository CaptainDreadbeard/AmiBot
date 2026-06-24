# AmiBot 🤖  
A small, personality‑driven CLI chatbot with memory, emotions, and a few secrets.

AmiBot is a lightweight command‑line chatbot written in Python.  
It remembers things you tell it, adapts its emotional tone, supports multiple personality modes, and includes fun utilities like jokes, dice rolls, definitions, and more.

It’s not machine learning — it’s handcrafted logic, personality tables, and memory structures — but that’s exactly what makes it charming, hackable, and easy to extend.

---

## ✨ Features

- **Short‑term memory** (recent messages)
- **Long‑term memory** stored in your OS‑native app data folder  
  - Windows: `%APPDATA%\amibot\longterm_memory.json`
  - macOS: `~/Library/Application Support/amibot/`
  - Linux: `~/.local/share/amibot/`
- **Personality modes**: friendly, serious, chaotic, sarcastic
- **Emotion detection** (positive / negative / neutral)
- **Conversation callbacks** (AmiBot brings up past topics)
- **Fun commands**: jokes, dice rolls, coin flips, definitions
- **A hidden easter egg** when you ask `/whoami` with no stored facts 😉

---

## 🚀 Installation

AmiBot can be installed from a local wheel or (eventually) from PyPI.

### Install from a wheel:

```bash
python -m pip install amibot-1.0.0-py3-none-any.whl

Run Amibot
amibot
If your PATH is set correctly, AmiBot will launch immediately.

General
Command	Description
/help	Show all commands
/stats	Show internal state (mode, emotion, memory)
/mode <type>	Change personality mode
/whoareyou	Show AmiBot’s identity
/whoami	Show what AmiBot remembers about you

Secret:  
If AmiBot has no long‑term facts stored, /whoami returns:
“The girls dem suga.”

Memory
Command	Description
/remember <fact>	Store a fact in long‑term memory
/clear_memory	Erase all long‑term memory

| Command | Description |
| --- | --- |
| ``/time`` | Show current time |
| ``/date`` | Show today’s date |
| ``/coin`` | Flip a coin |
| ``/roll`` | Roll a 6‑sided die |
| ``/joke`` | Tell a random joke |
| ``/define ``<word>`` | Define a simple word |

project structure

amibot/
  engine/
    core.py
    personality.py
  pyproject.toml
  README.md
  LICENSE

Development

git clone https://github.com/<your-username>/amibot.git
cd amibot
build the package--
python -m build
reinstall locally
python -m pip install --force-reinstall dist/*.whl

run:
amibot

