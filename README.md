# Cuayo Pet Desktop

---

## 🚀 Key Features

* **Absurd Movement**: Unlike a boring DVD logo, CUAYO has "states." It can idle, wander, or sprint across your desktop randomly.
* **Multi-Pet Madness**: Spawn an entire army of CUAYOs using the HQ Controller.
* **Context Awareness**: It’s watching you! CUAYO triggers a `rotate.mp3` surprise whenever it detects you opening or switching to a new application (e.g., Chrome, VS Code, or Folders).
* **Customizable Chaos**:
    * **Chaos Slider**: Adjust the speed from "Snail" to "Absolute Flash."
    * **Mute System**: For when you’re in a meeting but still want the visual madness.
    * **Population Control**: Instantly add (`+`) or remove (`-`) pets via the GUI.

---

## 🛠️ Installation & Setup

Ensure you have **Python 3.10+** installed on your system.

### 1. Install Dependencies
Open your terminal/command prompt and run:
```bash
pip install pillow pygame pygetwindow pyrect

```

### 2. Folder Structure

Ensure your directory is organized as follows:

```text
CUAYO_Project/
├── Img/
│   ├── leftNormal.png
│   ├── rightNormal.png
│   ├── leftBounce.png
│   └── rightBounce.png
├── soundEffect/
│   ├── bounced.mp3
│   ├── coayo1.mp3
│   └── rotate.mp3
├── main.py
└── README.md

```

### 3. Run the App

Launch the application by running:

```bash
python main.py

```

---

## 🎮 Controls

| Action | Control |
| --- | --- |
| **Spawn/Despawn** | Use the `+` and `-` buttons on the HQ Panel |
| **Adjust Speed** | Move the **Chaos Slider** in the HQ Panel |
| **Silence Mode** | Toggle the **Mute** button |
| **Individual Dismiss** | **Right-Click** directly on a CUAYO character |
| **Emergency Stop** | Click **CLOSE ALL** in the HQ Panel |

---

## ⚠️ Disclaimer

This application is have a big sound

---

*Developed with pure absurdity.*

```

---

##Personal Note: 
*I don't really care if you sell or reuse this code,*
*but you can add new features if you want xD.*