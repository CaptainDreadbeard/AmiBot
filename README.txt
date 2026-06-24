# AmiBot

AmiBot is a tiny, personality‑driven CLI chatbot written in Python.  
It remembers things you tell it, maintains emotional tone, supports multiple conversation topics, and stores long‑term memory on disk.

## Features

- **Conversational personality** with keyword‑based emotional responses  
- **Topic engine** (e.g., ice cream flavor conversations)  
- **Short‑term memory** (last 5 messages)  
- **Long‑term memory** saved to disk  
- **Persistent bot state** (mode + emotion survive restarts)  
- **CLI commands**  
  - `/time` — show current time  
  - `/date` — show current date  
  - `/joke` — random joke  
  - `/roll` — roll a die  
  - `/coin` — flip a coin  
  - `/remember <fact>` — store a long‑term fact  
  - `/clear_memory` — wipe long‑term memory  
  - `/stats` — show internal state  
  - `/mode <type>` — switch personality mode  
  - `/whoami` — show remembered facts  
  - `/whoareyou` — show bot info  

## Installation

```bash
pip install amibot
or install from source
python -m pip install dist/amibot-*.whl


Usage:
amibot

Project structure:
amibot/
    core.py
    personality.py
pyproject.toml
README.md
LICENSE



