# Windrose Server Manager Enhanced

A dedicated server manager for [Windrose](https://store.steampowered.com/app/3041230/Windrose/)

---

## Features

- **Steam and SteamCMD support with ability to switch**
- **Install Wizard** — When first launching the Server Manager you will be guided on how to get your dedicated server up and running via Steam or SteamCMD
- **One-click Start / Stop / Restart**
- **Easily Update Server Files**
- **Live dashboard** — CPU usage, RAM, player count, uptime, and connected player list
- **Live log viewer** — color-coded, filterable (All / Players / Warnings / Errors) with auto-scroll
- **Config editor** — Edit Server and Gameplay settings directly from the manager
- **One-click world backup** — Zip your save data to a timestamped archive
- **Auto-backup** — Schedule automatic backups at 1, 4, 8, 16, or 24-hour intervals
- **Scheduled daily restart** — set a time; manager restarts the server automatically
- **Auto-restart on crash** — Relaunches automatically if the server is not running
- **Player history** — persistent log of who joined and left
- **Invite code share** — Copies a ready-to-send message to clipboard
- **Self-updater** — checks GitHub for latest version and updates
---

## Requirements

- Windows 10 or Windows 11
- **Windrose** owned and installed via Steam or SteamCMD

> If using Steam, The dedicated server files are bundled inside the Windrose game install. You do not need a separate dedicated server download.

---

### How to Run

1. **Download the latest version**:
   ```
   https://github.com/Andrew1175/Windrose-Server-Manager-Enhanced/releases
   ```
2. **Run `Windrose-Server-Manager.exe`**
3. Follow the Setup Wizard to configure a new dedicated server or to use your pre-existing one.
4. Click **Install Server** — Only if using SteamCMD.
5. Switch to the **Dashboard** tab and click **Start**.

---

## Application Guide

| Tab | What it does |
|---|---|
| **Dashboard** | Live stats, player list, auto-restart toggle, save-on-stop option |
| **Config** | Edit `ServerDescription.json` and `WorldDescription.json` via form fields and sliders |
| **Log** | Live-tailing server log with color coding and filters (All / Players / Warnings / Errors) |
| **Tools** | Manual and auto backup, scheduled restart, restart countdown, player history, update the manager, patch notes |
| **Install** | Configure your server directories, update the server, verify it's installed properly |

---

## Config Files

Easily modify your Server and Gameplay Configurations:

| File | Location | Purpose |
|---|---|---|
| `ServerDescription.json` | `R5\` | Server name, max players, password, hosting IP, port. |
| `WorldDescription.json` | `R5\Saved\SaveProfiles\...\Worlds\<id>\` | Difficulty presets and all gameplay multipliers |

---

## Contributers

Original GUI and Design By: (https://github.com/psbrowand/Windrose-Server-Manager)
