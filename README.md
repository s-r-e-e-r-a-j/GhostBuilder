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

## Signing, Zipalign and Dry-run 

**Sign & zipalign? (y/N):**

If you choose `yes`, the tool will sign the APK (add a digital certificate) and run zipalign so the APK is ready for installation. If you choose `no`, the APK will not be signed and may not install on some devices.

**Final name:**

The file name you want for the finished APK (for example `final.apk`). This is the signed and aligned file the user will install.

**Enter keystore password / Re-enter new password:**

A keystore is a protected file that holds the signing key. You must enter a password to create it and confirm it. You will need this password again later to sign APKs with that keystore.

**These questions appear when creating a new keystore. They collect identity information for the signing certificate:**

- **What is your first and last name:** your name or organization name

- **What is the name of your organizational unit:** team or department (optional)

- **What is the name of your organization:** company or group name (optional)

- **What is the name of your City or Locality:** your city name (optional)

- **What is the name of your State or Province:** your state or region name

- **What is the two-letter country code for this unit:** country code (e.g., `us`, `in`)

**Confirmation (Is CN=..., OU=..., etc. correct?):**

Keytool shows what you entered and asks you to confirm. Answer `yes` if it looks correct.

**Enter Passphrase for keystore:**

Used again when signing the APK to confirm your keystore password.

**Dry run? (y/N):**

`Yes` (dry run): the tool only shows what it would do (preview). No files are created or changed.

`No`: the tool performs the real actions and writes files.
