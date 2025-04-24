# 🎧 Python SoundBoard App

> 🎼 A customizable soundboard built with Python — perfect for creators, streamers, and sound lovers! Trigger sound effects via hotkeys with fade, loop, and volume control.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![UI](https://img.shields.io/badge/UI-CustomTkinter-darkgreen)

---

## 🎯 About This App

This is a program created to play sound files based on specific key bindings set by the user. Built with Python using external libraries like **Pygame** and **Tkinter**, it supports:

- Adding various music/audio files (`.mp3`, `.wav`, `.ogg`, `.flac`)
- Assigning global hotkeys for quick sound playback
- Adjusting **individual volume levels**
- Enabling **looping** and **fade effects**
- Controlling **master volume**
- **Saving and loading presets** for future use

---

## ✨ Features

- ➕ Add audio files (`.mp3`, `.wav`, `.ogg`, `.flac`) and bind them to keys
- ⌨️ Custom hotkey support (e.g., `F1`, `Ctrl+Shift+A`)
- 🎚 Per-sound and master volume control
- 🔁 Looping support for continuous playback
- 🎚 Optional fade-out effect when stopping sounds
- 💾 Save and load your soundboard setup using `.sb` files
- 📁 Custom `.sb` file extension for configuration presets
- 🖥 Modern dark-themed interface built with CustomTkinter

---

## 🚀 Getting Started

### 🧾 Prerequisites

- Python 3.8 or later

### 🛠 Installation

1. **Clone this repo**

```bash
git clone https://github.com/ChristianDeoManlangit/soundboard-app.git
cd soundboard-app
```

2. **Install dependencies**

```bash
pip install customtkinter pygame keyboard
```

3. **Run the App**

```bash
python SoundBoard.py
```

---

## 🧑‍💻 How to Use

- 🎵 Click `+ Add Sound` to choose an audio file
- 🧠 Assign a hotkey to trigger playback
- ▶️ Click `Play` or press the hotkey to toggle play/pause
- 🔁 Use checkboxes to loop or fade
- 🔊 Change individual or master track volume with slider
- 📼 Save/Load your full soundboard setup

---

## 🖼 Screenshots

| Empty UI | Loading a File |
|-----------|------------------------|
| ![Empty UI](https://framerusercontent.com/images/5fb2HpvtQJHxt54Zvtic00pmiyo.png) | ![Loading a File](https://framerusercontent.com/images/0GlSpOApWQEynESe6iSHqPuZ4E.png) |

| Setting Hotkeys | With Music Files |
|--------|-----------------|
| ![Setting Hotkeys](https://framerusercontent.com/images/iQIJRXoiFf5osbPm2f9Ys2IaGiQ.png) | ![With Music Files](https://framerusercontent.com/images/B4u2MW9lQxhVbslMdcnNnY17bg.png) |


---

## ⚠️ Notes

- Some systems may require **admin rights** for hotkeys to work
- Ensure no duplicate hotkeys are assigned

---

## 📦 Build as Executable

Optional step using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed SoundBoard.py
```

---

## 👤 Author

Made with ❤️ by **[Deo aka Chai](https://github.com/ChristianDeoManlangit)**  

---
