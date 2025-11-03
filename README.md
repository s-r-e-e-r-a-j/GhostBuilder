## GhostBuilder

GhostBuilder is a payload generator tool for creating Android, Windows, Linux, macOS, and iOS payloads using **Metasploit**.
It can also inject payloads into existing APK files and sign them automatically.

It’s designed for **ethical hacking**, **penetration testing**, and **security research** — not for illegal use.

## Features

- Create payloads for Android, Windows, Linux, macOS, and iOS

- Inject payloads into real APKs

- Auto-install and check missing dependencies

- Sign and zipalign Android APKs

- Simple menu-based interface

## Requirements

GhostBuilder needs the following tools:

- `msfvenom`

- `msfconsole`

- `apktool`

- `zipalign`

- `jarsigner`

- `keytool`

- `aapt`

- `apksigner`

If any are missing, GhostBuilder can install them automatically.

## Installation
1. **Clone the repository:**
```bash
git clone https://github.com/s-r-e-e-r-a-j/GhostBuilder.git
```
2. **Navigate to the GhostBuilder directory:**
```bash
cd GhostBuilder
```
3. **Give execute permission to the `run.sh` script:**
```bash
chmod +x run.sh
```
## Usage

Run the tool:
```bash
./run.sh
```
Then select an option from the menu:
```bash
[1] Android -> Normal APK
[2] Android -> Inject into original APK
[3] Windows payload
[4] Linux payload
[5] macOS payload
[6] iOS payload
[7] Re-check dependencies
[8] Exit
```
GhostBuilder will guide you step by step — just enter:

- LHOST (your IP)

- LPORT (port number)

- Output file name

You can also sign the APK automatically after building.
